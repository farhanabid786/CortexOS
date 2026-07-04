import json
from typing import Dict, Any, Tuple
from app.agents.base import BaseAgent

class SoftwareArchitect(BaseAgent):
    def __init__(self):
        super().__init__("Software Architect", "System Architect")

    async def run(self, project_id: int, context: Dict[str, Any], db_session=None) -> Tuple[Dict[str, Any], str]:
        await self.log(project_id, "Formulating system architecture...", "INFO", db_session)
        
        prd = context.get("prd", {})
        
        json_out = None
        if self.api_key:
            try:
                await self.log(project_id, "Calling Gemini API to design software architecture...", "INFO", db_session)
                system_instruction = (
                    "You are an expert Software Architect. Design the tech stack, components, pattern, and directory structure. "
                    "Output ONLY a valid JSON containing: architectural_pattern, tech_stack (object with keys frontend, backend, "
                    "database), components (list of objects with name, description), directory_structure (nested dictionary representation)."
                )
                raw_response = await self.call_gemini(system_instruction, json.dumps(prd))
                json_out = json.loads(self.clean_json_string(raw_response))
            except Exception as e:
                await self.log(project_id, f"Gemini API execution failed, falling back to simulated architecture. Detail: {str(e)}", "WARNING", db_session)
                
        if not json_out:
            await self.log(project_id, "Using Mock Fallback mode to build system architecture.", "INFO", db_session)
            json_out = {
                "architectural_pattern": "Three-Tier Layered Architecture (MVC / Client-Server)",
                "tech_stack": {
                    "frontend": "React + TypeScript + Tailwind CSS + Framer Motion",
                    "backend": "FastAPI (Python) + SQLAlchemy",
                    "database": "PostgreSQL (SQLite fallback for local)",
                    "caching_queues": "Redis + Celery (Optional)"
                },
                "components": [
                    {"name": "Client App", "description": "Single Page React Application serving visual UI and state management"},
                    {"name": "API Gateway", "description": "FastAPI router handling CORS, Rate Limiting, and JWT Session authorization"},
                    {"name": "Core Pipeline Service", "description": "Asynchronous tasks and operational orchestration logic"},
                    {"name": "Data Access Layer", "description": "SQLAlchemy ORM mapped to local database engines"}
                ],
                "directory_structure": {
                    "backend": {
                        "app": {
                            "core": ["config.py", "database.py", "security.py"],
                            "models": ["__init__.py", "core_models.py"],
                            "api": ["auth.py", "pipelines.py"],
                            "services": ["scheduler.py"]
                        }
                    },
                    "frontend": {
                        "src": {
                            "components": ["Timeline.tsx", "Viewer.tsx"],
                            "pages": ["Dashboard.tsx", "Wizard.tsx"],
                            "context": ["AuthContext.tsx"]
                        }
                    }
                }
            }

        # Helper to generate tree-like string from dict
        def dict_to_tree_str(d: dict, indent: int = 0) -> str:
            tree = ""
            for k, v in d.items():
                tree += "  " * indent + f"├── {k}/\n"
                if isinstance(v, dict):
                    tree += dict_to_tree_str(v, indent + 1)
                elif isinstance(v, list):
                    for item in v:
                        tree += "  " * (indent + 1) + f"└── {item}\n"
            return tree

        dir_tree = dict_to_tree_str(json_out.get("directory_structure", {}))
        
        # Generate Markdown description
        markdown_out = f"""# System Architecture Blueprint

## Architectural Pattern
**{json_out.get('architectural_pattern', 'N/A')}**

## Selected Tech Stack
*   **Frontend:** {json_out.get('tech_stack', {}).get('frontend', 'N/A')}
*   **Backend:** {json_out.get('tech_stack', {}).get('backend', 'N/A')}
*   **Database:** {json_out.get('tech_stack', {}).get('database', 'N/A')}

## Component Definitions
{chr(10).join([f"*   **{c.get('name')}:** {c.get('description')}" for c in json_out.get('components', [])])}

## Codebase Directory Structure
```text
{dir_tree or "N/A"}
```
"""
        await self.log(project_id, "System architecture designed successfully.", "SUCCESS", db_session)
        return json_out, markdown_out
