from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.core.security import detect_prompt_injection, log_audit_action
from app.api.deps import get_current_active_user
from app.models import User, Project
from app.schemas import ProjectCreate, ProjectResponse
from app.agents.orchestrator import orchestrator

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    request: Request,
    project_in: ProjectCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    # 1. Prompt Injection Scan
    is_injection, reason = detect_prompt_injection(project_in.prompt)
    if is_injection:
        await log_audit_action(
            db, "PROMPT_INJECTION_BLOCKED", user_id=current_user.id, ip_address=request.client.host,
            status_code=400, details=f"Block prompt injection attempt. Reason: {reason}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Security Validation Exception: {reason}"
        )
        
    # 2. Save Project metadata
    db_project = Project(
        title=project_in.title,
        description=project_in.description,
        prompt=project_in.prompt,
        user_id=current_user.id,
        status="pending"
    )
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    
    await log_audit_action(
        db, "PROJECT_CREATE_SUCCESS", user_id=current_user.id, ip_address=request.client.host,
        status_code=201, details=f"Created project {db_project.id} with title: {db_project.title}"
    )
    
    # 3. Trigger Orchestrator Background Pipeline task
    background_tasks.add_task(orchestrator.run_pipeline, db_project.id)
    
    return db_project

@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Project).filter(Project.user_id == current_user.id).order_by(Project.created_at.desc())
    )
    return result.scalars().all()

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Project).filter(Project.id == project_id, Project.user_id == current_user.id)
    )
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    request: Request,
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Project).filter(Project.id == project_id, Project.user_id == current_user.id)
    )
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    await db.delete(project)
    await db.commit()
    
    await log_audit_action(
        db, "PROJECT_DELETE_SUCCESS", user_id=current_user.id, ip_address=request.client.host,
        status_code=204, details=f"Deleted project {project_id}"
    )
    return None
