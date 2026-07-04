import json
from typing import Dict, Any, Tuple
from app.agents.base import BaseAgent
from app.core.security import detect_prompt_injection

class RequirementAnalyst(BaseAgent):
    def __init__(self):
        super().__init__("Requirement Analyst", "Product Analyst")

    async def run(self, project_id: int, context: Dict[str, Any], db_session=None) -> Tuple[Dict[str, Any], str]:
        await self.log(project_id, "Initializing requirements analysis...", "INFO", db_session)
        
        prompt = context.get("prompt", "")
        title = context.get("title", "")
        
        # Security scan
        is_injection, reason = detect_prompt_injection(prompt)
        if is_injection:
            await self.log(project_id, f"Security Alert: Potential prompt injection detected. Reason: {reason}", "ERROR", db_session)
            raise ValueError(f"Prompt injection validation failed: {reason}")
            
        await self.log(project_id, "Security scanning complete. Prompt is clean.", "SUCCESS", db_session)
        
        json_out = None
        if self.api_key:
            try:
                await self.log(project_id, "Calling Gemini API to analyze requirements...", "INFO", db_session)
                system_instruction = (
                    "You are an expert Requirement Analyst. Analyze the user's software idea and generate a structured JSON "
                    "containing: project_title, scope_statement, functional_requirements (list), non_functional_requirements (list), "
                    "target_personas (list), and out_of_scope (list). Provide ONLY a JSON object containing these keys."
                )
                raw_response = await self.call_gemini(system_instruction, f"Title: {title}\nPrompt: {prompt}")
                json_out = json.loads(self.clean_json_string(raw_response))
            except Exception as e:
                await self.log(project_id, f"Gemini API execution failed, falling back to simulated output. Detail: {str(e)}", "WARNING", db_session)
                
        if not json_out:
            # Fallback to simulated high-quality mock output
            await self.log(project_id, "Using Mock Fallback mode to analyze requirements.", "INFO", db_session)
            json_out = {
                "project_title": title,
                "scope_statement": f"Build a production-ready application for: {title}. It addresses: {prompt[:100]}...",
                "functional_requirements": [
                    "User Authentication (Register, Login, Session)",
                    f"Core System Operations relating to {title}",
                    "Audit Logging and Security validation",
                    "Data visualization and reporting views"
                ],
                "non_functional_requirements": [
                    "Low latency under 200ms for API calls",
                    "Robust security using industry standard JWT tokens",
                    "High responsiveness on mobile and desktop platforms"
                ],
                "target_personas": ["System Administrator", "Active Business User", "Developer Integration Officer"],
                "out_of_scope": ["Multi-regional replication", "Third-party payment settlement systems"]
            }
            
        # Generate Markdown description
        markdown_out = f"""# Requirement Analysis: {json_out.get('project_title', title)}
Base User Prompt: {prompt}

## Scope Statement
{json_out.get('scope_statement', 'N/A')}

## Target Personas
{chr(10).join([f'- {p}' for p in json_out.get('target_personas', [])])}

## Functional Requirements
{chr(10).join([f'- {r}' for r in json_out.get('functional_requirements', [])])}

## Non-Functional Requirements
{chr(10).join([f'- {r}' for r in json_out.get('non_functional_requirements', [])])}

## Out of Scope
{chr(10).join([f'- {r}' for r in json_out.get('out_of_scope', [])])}
"""
        await self.log(project_id, "Completed requirement analysis and generated specification.", "SUCCESS", db_session)
        return json_out, markdown_out
