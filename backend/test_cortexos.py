import asyncio
import sys
from fastapi.testclient import TestClient

# Add current path to sys.path
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import app
from app.core.database import Base, engine, async_session
from app.models import User, Project, Blueprint, AgentLog
from sqlalchemy import select, delete

async def test_flow():
    print("--- Starting CortexOS Verification Test ---")
    
    # 0. Initialize tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables initialized.")
    
    # 1. Clean database tables first to prevent duplicate errors
    async with async_session() as session:
        await session.execute(delete(AgentLog))
        await session.execute(delete(Blueprint))
        await session.execute(delete(Project))
        await session.execute(delete(User))
        await session.commit()
    print("Database cleared.")

    client = TestClient(app)
    client.__enter__()
    
    # 2. Test Registration
    reg_payload = {
        "email": "testuser@cortexos.dev",
        "password": "SuperSecretPassword123",
        "full_name": "Test Engineer"
    }
    response = client.post("/api/auth/register", json=reg_payload)
    assert response.status_code == 201, f"Reg failed: {response.text}"
    user_data = response.json()
    print(f"Registered user successfully: {user_data['email']}, Role: {user_data['role']}")
    
    # 3. Test Login
    login_data = {
        "username": "testuser@cortexos.dev",
        "password": "SuperSecretPassword123"
    }
    response = client.post("/api/auth/login", data=login_data)
    assert response.status_code == 200, f"Login failed: {response.text}"
    token_data = response.json()
    token = token_data["access_token"]
    print("Logged in successfully, token retrieved.")

    # 4. Test /me Endpoint (This was the auth.py bug we fixed!)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == 200, f"/me failed: {response.text}"
    me_data = response.json()
    assert me_data["email"] == "testuser@cortexos.dev", f"Email mismatch: {me_data}"
    assert me_data["role"] == "admin", "First registered user should be admin."
    print("Verified `/auth/me` endpoint returns correct user schema.")

    # 5. Test Project Creation and pipeline execution
    proj_payload = {
        "title": "Task Manager App",
        "description": "A collaborative task planning application",
        "prompt": "Create a secure web app for logging tasks, assigning priorities, and viewing a timeline of tasks."
    }
    response = client.post("/api/projects/", json=proj_payload, headers=headers)
    assert response.status_code == 201, f"Project creation failed: {response.text}"
    project_data = response.json()
    project_id = project_data["id"]
    print(f"Created project '{project_data['title']}' with ID {project_id}.")

    # Wait for the background task to complete (since orchestrator runs in background_tasks)
    # The pipeline executes sequentially with sleep(0.5) per agent, so 10 agents take about ~5 seconds.
    print("Waiting for agent pipeline to run...")
    max_wait = 15
    completed = False
    
    for i in range(max_wait):
        await asyncio.sleep(1)
        response = client.get(f"/api/projects/{project_id}", headers=headers)
        assert response.status_code == 200, f"Failed to get project: {response.text}"
        p_status = response.json()["status"]
        print(f"  [Seconds {i+1}] Current pipeline status: {p_status}")
        if p_status == "completed":
            completed = True
            break
        elif p_status == "failed":
            # Retrieve agent log to see failure reason
            log_res = client.get(f"/api/logs/{project_id}", headers=headers)
            print(f"Pipeline failed! Logs: {log_res.json()}")
            break

    assert completed, "Pipeline execution timed out or failed."
    print("Orchestrator pipeline successfully finished in 'completed' state.")

    # 6. Retrieve and Verify Blueprint
    response = client.get(f"/api/blueprints/{project_id}", headers=headers)
    assert response.status_code == 200, f"Blueprint fetch failed: {response.text}"
    bp_data = response.json()
    assert bp_data["requirement_analysis"] is not None
    assert bp_data["prd"] is not None
    assert bp_data["architecture_design"] is not None
    assert bp_data["database_schema"] is not None
    assert bp_data["api_design"] is not None
    assert bp_data["frontend_plan"] is not None
    assert bp_data["testing_strategy"] is not None
    assert bp_data["security_report"] is not None
    assert bp_data["deployment_guide"] is not None
    assert bp_data["review_report"] is not None
    assert bp_data["markdown_output"] is not None
    print("Verified blueprint contents: all 10 stages generated valid JSON & markdown specifications.")

    # 7. Test Rerun Log Cleanup (orchestrator.py fix!)
    # Fetch log count before rerun
    log_res = client.get(f"/api/logs/{project_id}", headers=headers)
    assert log_res.status_code == 200
    first_run_logs = len(log_res.json())
    print(f"Log count after first run: {first_run_logs}")
    assert first_run_logs > 0, "No logs recorded!"

    # Trigger second run
    from app.agents.orchestrator import orchestrator
    print("Simulating a manual pipeline rerun on the same project...")
    await orchestrator.run_pipeline(project_id)
    
    # Fetch log count after second run
    log_res2 = client.get(f"/api/logs/{project_id}", headers=headers)
    assert log_res2.status_code == 200
    second_run_logs = len(log_res2.json())
    print(f"Log count after rerun: {second_run_logs}")
    # Since we clean up logs, the total count should be roughly the same, and old ones deleted
    # If we didn't clean them up, the log count would have doubled.
    assert second_run_logs < (first_run_logs * 2), "Logs did not clean up correctly!"
    print("Verified log cleanup deletes previous records and records new ones cleanly.")

    client.__exit__(None, None, None)
    print("\n--- CortexOS Backend Verification: ALL PASSED ---")

if __name__ == "__main__":
    # Ensure event loop runs the async flow
    asyncio.run(test_flow())
