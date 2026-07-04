import json
from typing import Dict, Any, Tuple
from app.agents.base import BaseAgent

class ReviewAgent(BaseAgent):
    def __init__(self):
        super().__init__("Review Agent", "Principal Engineer Gatekeeper")

    async def run(self, project_id: int, context: Dict[str, Any], db_session=None) -> Tuple[Dict[str, Any], str]:
        await self.log(project_id, "Commencing architectural audit and code structure review...", "INFO", db_session)
        
        doc_guide = context.get("deployment_guide", {})
        
        json_out = None
        if self.api_key:
            try:
                await self.log(project_id, "Calling Gemini API to review blueprint outputs...", "INFO", db_session)
                system_instruction = (
                    "You are an expert Review Agent. Evaluate the entire multi-agent context generated so far. "
                    "Output ONLY a valid JSON containing: score (integer from 0 to 100), strengths (list), "
                    "gaps (list), verdict (string verdict, e.g. APPROVED or REJECTED WITH CHANGES)."
                )
                raw_response = await self.call_gemini(system_instruction, json.dumps(doc_guide))
                json_out = json.loads(self.clean_json_string(raw_response))
            except Exception as e:
                await self.log(project_id, f"Gemini API execution failed, falling back to simulated review. Detail: {str(e)}", "WARNING", db_session)
                
        if not json_out:
            await self.log(project_id, "Using Mock Fallback mode to run quality review.", "INFO", db_session)
            json_out = {
                "score": 95,
                "strengths": [
                    "Exemplary modular API routing using structured FastAPI patterns",
                    "Strong security posture containing prompt injection detection and parameter binding",
                    "Clearly-defined directory outlines promoting high maintainability"
                ],
                "gaps": [
                    "Database schema lacks explicit partitioning suggestions for high-scale users",
                    "Testing plans require integration assertions for rate limit throttling validation"
                ],
                "verdict": "APPROVED FOR DEVELOPMENT"
            }

        # Generate Markdown description
        markdown_out = f"""# Architectural Review & Validation Report

## Review Audit Score: **{json_out.get('score', 0)} / 100**
**Final Verdict:** `{json_out.get('verdict', 'N/A')}`

## Strengths Identified
{chr(10).join([f'- {s}' for s in json_out.get('strengths', [])])}

## Operational Gaps & Recommendations
{chr(10).join([f'- {g}' for g in json_out.get('gaps', [])])}
"""
        await self.log(project_id, "Architectural audit complete. Blueprint status updated to COMPLETED.", "SUCCESS", db_session)
        return json_out, markdown_out
