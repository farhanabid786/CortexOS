import json
from typing import Dict, Any, Tuple
from app.agents.base import BaseAgent

class ProductManager(BaseAgent):
    def __init__(self):
        super().__init__("Product Manager", "Product Manager")

    async def run(self, project_id: int, context: Dict[str, Any], db_session=None) -> Tuple[Dict[str, Any], str]:
        await self.log(project_id, "Initializing PRD generation...", "INFO", db_session)
        
        reqs = context.get("requirement_analysis", {})
        title = reqs.get("project_title", "Software Project")
        
        json_out = None
        if self.api_key:
            try:
                await self.log(project_id, "Calling Gemini API to generate PRD and User Stories...", "INFO", db_session)
                system_instruction = (
                    "You are an expert Product Manager. Create a Product Requirement Document (PRD) based on requirements. "
                    "Output ONLY a valid JSON containing: prd_version, objectives (list), user_stories (list of objects with keys "
                    "id, title, as_a, i_want_to, so_that), success_metrics (list)."
                )
                raw_response = await self.call_gemini(system_instruction, json.dumps(reqs))
                json_out = json.loads(self.clean_json_string(raw_response))
            except Exception as e:
                await self.log(project_id, f"Gemini API execution failed, falling back to simulated PRD. Detail: {str(e)}", "WARNING", db_session)
                
        if not json_out:
            await self.log(project_id, "Using Mock Fallback mode to build PRD.", "INFO", db_session)
            json_out = {
                "prd_version": "1.0.0",
                "objectives": [
                    f"Create an automated pipeline supporting the requirements of {title}",
                    "Optimize developer workflows through modular interfaces",
                    "Assure data persistence, compliance, and user accountability"
                ],
                "user_stories": [
                    {"id": "US-1", "title": "User Authentication", "as_a": "registered user", "i_want_to": "login securely", "so_that": "I can access my saved dashboards"},
                    {"id": "US-2", "title": "Data Pipeline Control", "as_a": "system analyst", "i_want_to": "run batch pipelines", "so_that": "I can evaluate calculations"},
                    {"id": "US-3", "title": "Audit Compliance", "as_a": "compliance auditor", "i_want_to": "view system logs", "so_that": "I can verify operational safety"}
                ],
                "success_metrics": [
                    "User retention index of over 85% in first month",
                    "Zero unauthorized API penetrations",
                    "Task processing speeds under 10 seconds"
                ]
            }
                
        # Generate Markdown description
        markdown_out = f"""# Product Requirement Document (PRD) - v{json_out.get('prd_version', '1.0.0')}

## Project Objectives
{chr(10).join([f'- {obj}' for obj in json_out.get('objectives', [])])}

## User Stories
| ID | Story Name | Description |
|---|---|---|
"""
        for story in json_out.get('user_stories', []):
            desc = f"As a **{story.get('as_a')}**, I want to **{story.get('i_want_to')}** so that **{story.get('so_that')}**."
            markdown_out += f"| {story.get('id')} | {story.get('title')} | {desc} |\n"
            
        markdown_out += f"""
## Success Metrics
{chr(10).join([f'- {metric}' for metric in json_out.get('success_metrics', [])])}
"""
        await self.log(project_id, "PRD and User Stories generated successfully.", "SUCCESS", db_session)
        return json_out, markdown_out
