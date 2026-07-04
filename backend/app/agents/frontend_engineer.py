import json
from typing import Dict, Any, Tuple
from app.agents.base import BaseAgent

class FrontendEngineer(BaseAgent):
    def __init__(self):
        super().__init__("Frontend Engineer", "Senior Frontend Engineer")

    async def run(self, project_id: int, context: Dict[str, Any], db_session=None) -> Tuple[Dict[str, Any], str]:
        await self.log(project_id, "Formulating frontend layout design...", "INFO", db_session)
        
        api_design = context.get("api_design", {})
        
        json_out = None
        if self.api_key:
            try:
                await self.log(project_id, "Calling Gemini API to design frontend structure...", "INFO", db_session)
                system_instruction = (
                    "You are an expert Frontend Engineer. Design the React component hierarchy, routes, global state, and styling. "
                    "Output ONLY a valid JSON containing: framework, routing (list of objects with path, component, guards), "
                    "global_state (list of objects with name, actions, description), component_hierarchy (list of objects with component, children)."
                )
                raw_response = await self.call_gemini(system_instruction, json.dumps(api_design))
                json_out = json.loads(self.clean_json_string(raw_response))
            except Exception as e:
                await self.log(project_id, f"Gemini API execution failed, falling back to simulated frontend design. Detail: {str(e)}", "WARNING", db_session)
                
        if not json_out:
            await self.log(project_id, "Using Mock Fallback mode to build frontend components.", "INFO", db_session)
            json_out = {
                "framework": "React (TypeScript) + Tailwind CSS + Framer Motion",
                "routing": [
                    {"path": "/", "component": "LandingPage", "guards": "None"},
                    {"path": "/login", "component": "AuthPage", "guards": "GuestOnly"},
                    {"path": "/dashboard", "component": "Dashboard", "guards": "RequireAuth"},
                    {"path": "/records/new", "component": "CreateRecordWizard", "guards": "RequireAuth"}
                ],
                "global_state": [
                    {"name": "AuthContext", "actions": ["login()", "logout()", "refresh()"], "description": "Stores current token and profile details"},
                    {"name": "ThemeContext", "actions": ["toggleTheme()"], "description": "Toggles dark/light visual modes"}
                ],
                "component_hierarchy": [
                    {
                        "component": "Layout",
                        "children": ["Navbar", "Sidebar", "Footer"]
                    },
                    {
                        "component": "Dashboard",
                        "children": ["StatSummaryCard", "RecentActivityList", "InteractiveChart"]
                    }
                ]
            }

        # Generate Markdown description
        markdown_out = f"""# Frontend Architecture Design

**Client Framework:** {json_out.get('framework', 'React (TypeScript)')}

## Global Context & State Management
{chr(10).join([f"- **{state.get('name')}:** {state.get('description')} (Methods: `{', '.join(state.get('actions', []))}`)" for state in json_out.get('global_state', [])])}

## Client-Side Application Routes
| Path | Component/Page | Security Guard |
|---|---|---|
"""
        for route in json_out.get('routing', []):
            markdown_out += f"| `{route.get('path')}` | `{route.get('component')}` | {route.get('guards')} |\n"

        markdown_out += "\n## Reusable Component Tree Hierarchy\n"
        for comp in json_out.get('component_hierarchy', []):
            markdown_out += f"- **`{comp.get('component')}`**\n"
            for child in comp.get('children', []):
                markdown_out += f"  - `└── {child}`\n"
            markdown_out += "\n"

        await self.log(project_id, "Frontend interface structures completed.", "SUCCESS", db_session)
        return json_out, markdown_out
