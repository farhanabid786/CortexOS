import json
from typing import Dict, Any, Tuple
from app.agents.base import BaseAgent

class BackendEngineer(BaseAgent):
    def __init__(self):
        super().__init__("Backend Engineer", "Senior Backend Engineer")

    async def run(self, project_id: int, context: Dict[str, Any], db_session=None) -> Tuple[Dict[str, Any], str]:
        await self.log(project_id, "Designing backend API routing structure...", "INFO", db_session)
        
        db_schema = context.get("database_schema", {})
        
        json_out = None
        if self.api_key:
            try:
                await self.log(project_id, "Calling Gemini API to design REST endpoints...", "INFO", db_session)
                system_instruction = (
                    "You are an expert Backend Engineer. Design the REST API endpoints, methods, inputs, and response payloads. "
                    "Output ONLY a valid JSON containing: base_url, endpoints (list of objects with path, method, summary, "
                    "query_params (optional list of objects with name, type, default), request_body (optional object), responses (object))."
                )
                raw_response = await self.call_gemini(system_instruction, json.dumps(db_schema))
                json_out = json.loads(self.clean_json_string(raw_response))
            except Exception as e:
                await self.log(project_id, f"Gemini API execution failed, falling back to simulated API design. Detail: {str(e)}", "WARNING", db_session)
                
        if not json_out:
            await self.log(project_id, "Using Mock Fallback mode to build backend routes.", "INFO", db_session)
            json_out = {
                "base_url": "/api/v1",
                "endpoints": [
                    {
                        "path": "/auth/register",
                        "method": "POST",
                        "summary": "Register new user account",
                        "request_body": {"email": "string", "password": "string", "full_name": "string"},
                        "responses": {
                            "201": {"description": "User created successfully", "content": {"id": "int", "email": "string"}},
                            "400": {"description": "Validation error / Email already exists"}
                        }
                    },
                    {
                        "path": "/auth/login",
                        "method": "POST",
                        "summary": "Authenticate user and get JWT",
                        "request_body": {"username": "string (email)", "password": "string"},
                        "responses": {
                            "200": {"content": {"access_token": "string", "token_type": "string"}},
                            "401": {"description": "Invalid credentials"}
                        }
                    },
                    {
                        "path": "/records",
                        "method": "GET",
                        "summary": "List user's records with pagination",
                        "query_params": [{"name": "skip", "type": "int", "default": 0}, {"name": "limit", "type": "int", "default": 10}],
                        "responses": {
                            "200": {"content": "array of record objects"},
                            "401": {"description": "Unauthorized"}
                        }
                    }
                ]
            }

        # Generate Markdown description
        markdown_out = f"""# Backend REST API Design Specification

**Base API Endpoint:** `{json_out.get('base_url', '/api/v1')}`

"""
        for ep in json_out.get('endpoints', []):
            markdown_out += f"### `[{ep.get('method')}]` {ep.get('path')}\n"
            markdown_out += f"**Summary:** {ep.get('summary')}\n\n"
            
            if ep.get('query_params'):
                markdown_out += "**Query Parameters:**\n"
                for param in ep.get('query_params', []):
                    markdown_out += f"- `{param.get('name')}` ({param.get('type')}, default: `{param.get('default')}`)\n"
                markdown_out += "\n"
                
            if ep.get('request_body'):
                markdown_out += "**Request Body Payload:**\n"
                markdown_out += f"```json\n{json.dumps(ep.get('request_body'), indent=2)}\n```\n\n"
                
            markdown_out += "**Expected Responses:**\n"
            for code, resp in ep.get('responses', {}).items():
                desc = resp.get('description', 'Successful execution' if code == '200' or code == '201' else 'Error response')
                markdown_out += f"- **Code {code}**: {desc}\n"
                if resp.get('content'):
                    markdown_out += f"  ```json\n{json.dumps(resp.get('content'), indent=2)}\n  ```\n"
            markdown_out += "\n---\n"

        await self.log(project_id, "Backend endpoint routing design finalized.", "SUCCESS", db_session)
        return json_out, markdown_out
