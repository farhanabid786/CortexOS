import json
from typing import Dict, Any, Tuple
from app.agents.base import BaseAgent

class QAEngineer(BaseAgent):
    def __init__(self):
        super().__init__("QA Engineer", "QA Engineer")

    async def run(self, project_id: int, context: Dict[str, Any], db_session=None) -> Tuple[Dict[str, Any], str]:
        await self.log(project_id, "Formulating QA test scripts and strategy...", "INFO", db_session)
        
        frontend_plan = context.get("frontend_plan", {})
        
        json_out = None
        if self.api_key:
            try:
                await self.log(project_id, "Calling Gemini API to design testing strategies...", "INFO", db_session)
                system_instruction = (
                    "You are an expert QA Engineer. Design unit tests, integration tests, E2E scenarios, and select frameworks. "
                    "Output ONLY a valid JSON containing: testing_frameworks (object with keys backend, frontend), "
                    "unit_test_cases (list of objects with id, module, description), "
                    "integration_test_cases (list of objects with id, flow, description), "
                    "e2e_scenarios (list of objects with id, scenario, description)."
                )
                raw_response = await self.call_gemini(system_instruction, json.dumps(frontend_plan))
                json_out = json.loads(self.clean_json_string(raw_response))
            except Exception as e:
                await self.log(project_id, f"Gemini API execution failed, falling back to simulated testing plan. Detail: {str(e)}", "WARNING", db_session)
                
        if not json_out:
            await self.log(project_id, "Using Mock Fallback mode to build QA test plans.", "INFO", db_session)
            json_out = {
                "testing_frameworks": {
                    "backend": "pytest + pytest-asyncio + httpx (for client testing)",
                    "frontend": "Jest + React Testing Library + Playwright (for E2E)"
                },
                "unit_test_cases": [
                    {"id": "UT-01", "module": "Auth", "description": "Ensure password verification detects correct vs incorrect hashes"},
                    {"id": "UT-02", "module": "Security", "description": "Verify prompt injection detector catches ignore previous instructions override request"}
                ],
                "integration_test_cases": [
                    {"id": "IT-01", "flow": "Pipeline Run", "description": "Create project -> launch multi-agent sequence -> verify final blueprint status is completed"}
                ],
                "e2e_scenarios": [
                    {"id": "E2E-01", "scenario": "Standard Dashboard Navigation", "description": "Login -> Navigate to dashboard -> Create Project -> View timeline completion"}
                ]
            }

        # Generate Markdown description
        markdown_out = f"""# Quality Assurance Testing Strategy

## Recommended Testing Toolchain
*   **Backend Testing:** {json_out.get('testing_frameworks', {}).get('backend', 'N/A')}
*   **Frontend Testing:** {json_out.get('testing_frameworks', {}).get('frontend', 'N/A')}

## Unit Test Checklist
| Test ID | System Module | Test Verification |
|---|---|---|
"""
        for ut in json_out.get('unit_test_cases', []):
            markdown_out += f"| {ut.get('id')} | {ut.get('module')} | {ut.get('description')} |\n"

        markdown_out += "\n## System Integration Tests\n"
        for it in json_out.get('integration_test_cases', []):
            markdown_out += f"- **{it.get('id')}: {it.get('flow')}** - {it.get('description')}\n"

        markdown_out += "\n## End-to-End User Journeys (E2E)\n"
        for e2e in json_out.get('e2e_scenarios', []):
            markdown_out += f"- **{e2e.get('id')}: {e2e.get('scenario')}** - {e2e.get('description')}\n"

        await self.log(project_id, "QA test specifications compiled.", "SUCCESS", db_session)
        return json_out, markdown_out
