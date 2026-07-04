import json
from typing import Dict, Any, Tuple
from app.agents.base import BaseAgent

class SecurityAnalyst(BaseAgent):
    def __init__(self):
        super().__init__("Security Analyst", "Certified Security Analyst")

    async def run(self, project_id: int, context: Dict[str, Any], db_session=None) -> Tuple[Dict[str, Any], str]:
        await self.log(project_id, "Executing threat analysis scan...", "INFO", db_session)
        
        qa_strategy = context.get("testing_strategy", {})
        
        json_out = None
        if self.api_key:
            try:
                await self.log(project_id, "Calling Gemini API to audit security protocols...", "INFO", db_session)
                system_instruction = (
                    "You are an expert Security Analyst. Generate a STRIDE-based threat model and checklist for the system. "
                    "Output ONLY a valid JSON containing: security_level, threat_model (list of objects with category, threat, mitigation), "
                    "security_checklist (list)."
                )
                raw_response = await self.call_gemini(system_instruction, json.dumps(qa_strategy))
                json_out = json.loads(self.clean_json_string(raw_response))
            except Exception as e:
                await self.log(project_id, f"Gemini API execution failed, falling back to simulated security report. Detail: {str(e)}", "WARNING", db_session)
                
        if not json_out:
            await self.log(project_id, "Using Mock Fallback mode to build threat modeling matrix.", "INFO", db_session)
            json_out = {
                "security_level": "Tier-1 Production Compliant",
                "threat_model": [
                    {
                        "category": "Spoofing (Identity)",
                        "threat": "Adversaries intercepting session authentication",
                        "mitigation": "Enforce HTTPS transmission and short JWT lifetimes with secure HttpOnly cookie tokens"
                    },
                    {
                        "category": "Information Disclosure",
                        "threat": "Logging stack trace or environment variables in logs",
                        "mitigation": "Disable debug mode in production; implement structured logging masking sensitive info"
                    },
                    {
                        "category": "Denial of Service",
                        "threat": "Spamming computational pipelines to crash backend systems",
                        "mitigation": "Implement rate limiting middleware and background tasks processing queues"
                    }
                ],
                "security_checklist": [
                    "Hash passwords using Passlib's bcrypt with work factor 12",
                    "Sanitize all text inputs using prompt injection checkers",
                    "Ensure SQL statements use SQLAlchemy parameterized bindings"
                ]
            }

        # Generate Markdown description
        markdown_out = f"""# Security Vulnerability & Threat Report

**Security Tier Rating:** `{json_out.get('security_level', 'N/A')}`

## Threat Modeling Matrix (STRIDE)
| Threat Category | Potential Attack Vector | Applied Mitigation |
|---|---|---|
"""
        for threat in json_out.get('threat_model', []):
            markdown_out += f"| {threat.get('category')} | {threat.get('threat')} | {threat.get('mitigation')} |\n"

        markdown_out += "\n## Security hardening checklist\n"
        for item in json_out.get('security_checklist', []):
            markdown_out += f"- [ ] {item}\n"

        await self.log(project_id, "Security report created successfully.", "SUCCESS", db_session)
        return json_out, markdown_out
