import json
from typing import Dict, Any, Tuple
from app.agents.base import BaseAgent

class DocumentationAgent(BaseAgent):
    def __init__(self):
        super().__init__("Documentation Agent", "Technical Writer")

    async def run(self, project_id: int, context: Dict[str, Any], db_session=None) -> Tuple[Dict[str, Any], str]:
        await self.log(project_id, "Compiling setup and deployment documentation...", "INFO", db_session)
        
        sec_report = context.get("security_report", {})
        
        json_out = None
        if self.api_key:
            try:
                await self.log(project_id, "Calling Gemini API to construct deployment manuals...", "INFO", db_session)
                system_instruction = (
                    "You are an expert Technical Writer. Design a comprehensive deployment and README setup guide. "
                    "Output ONLY a valid JSON containing: prerequisites (list), local_setup_steps (list), "
                    "docker_command, environment_variables (list of objects with name, description)."
                )
                raw_response = await self.call_gemini(system_instruction, json.dumps(sec_report))
                json_out = json.loads(self.clean_json_string(raw_response))
            except Exception as e:
                await self.log(project_id, f"Gemini API execution failed, falling back to simulated deployment manuals. Detail: {str(e)}", "WARNING", db_session)
                
        if not json_out:
            await self.log(project_id, "Using Mock Fallback mode to build deployment manuals.", "INFO", db_session)
            json_out = {
                "prerequisites": ["Python 3.10+", "Node.js 18+", "PostgreSQL (Optional)"],
                "local_setup_steps": [
                    "git clone <repository_url> && cd project",
                    "python -m venv venv && source venv/bin/activate (on Linux/macOS) or venv\\Scripts\\activate (on Windows)",
                    "pip install -r backend/requirements.txt",
                    "cd frontend && npm install && npm run dev",
                    "Configure backend/.env with your GEMINI_API_KEY and database URL"
                ],
                "docker_command": "docker compose up --build",
                "environment_variables": [
                    {"name": "DATABASE_URL", "description": "SQL Database connection string"},
                    {"name": "JWT_SECRET_KEY", "description": "Secret token validation seed"},
                    {"name": "GEMINI_API_KEY", "description": "Google Generative AI Access Key"}
                ]
            }

        # Generate Markdown description
        markdown_out = f"""# Deployment & Setup Manual

## Project Prerequisites
{chr(10).join([f'- {p}' for p in json_out.get('prerequisites', [])])}

## Environment Configurations
| Variable | Description |
|---|---|
"""
        for env in json_out.get('environment_variables', []):
            markdown_out += f"| `{env.get('name')}` | {env.get('description')} |\n"

        markdown_out += f"""
## Local Machine Launch (Step-by-Step)
{chr(10).join([f'{i+1}. {step}' for i, step in enumerate(json_out.get('local_setup_steps', []))])}

## Production Docker Launch
Run the following in the root folder:
```bash
{json_out.get('docker_command', 'docker-compose up --build')}
```
"""
        await self.log(project_id, "Project documents compiled.", "SUCCESS", db_session)
        return json_out, markdown_out
