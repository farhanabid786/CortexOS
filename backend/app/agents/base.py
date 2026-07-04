import json
import logging
import re
import asyncio
from typing import Dict, Any, Tuple, Optional
import httpx
from app.core.config import settings

logger = logging.getLogger("cortexos.agents")

class BaseAgent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.api_key = settings.GEMINI_API_KEY
        self.model = "gemini-2.5-flash" # Default Gemini model

    async def log(self, project_id: int, message: str, level: str = "INFO", db_session=None):
        """
        Log to console and optionally to database `AgentLog` table.
        """
        log_msg = f"[{self.name}] {message}"
        if level == "INFO":
            logger.info(log_msg)
        elif level == "WARNING":
            logger.warning(log_msg)
        elif level == "ERROR":
            logger.error(log_msg)
        elif level == "SUCCESS":
            logger.info(f"SUCCESS: {log_msg}")
            
        if db_session:
            from app.models import AgentLog
            db_log = AgentLog(
                project_id=project_id,
                agent_name=self.name,
                log_level=level,
                message=message
            )
            db_session.add(db_log)
            await db_session.commit()

    async def call_gemini(self, system_instruction: str, prompt: str) -> str:
        """
        Calls Gemini API using standard HTTP REST interface for maximum reliability,
        supporting structured output generation.
        """
        if not self.api_key:
            # Running in Mock fallback mode
            raise ValueError("GEMINI_API_KEY not configured")
            
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": f"{system_instruction}\n\nUser Input / Context:\n{prompt}"}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "topP": 0.95,
                "topK": 40,
                "maxOutputTokens": 8192,
            }
        }
        
        max_retries = 3
        retry_delay = 5.0
        
        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.post(url, headers=headers, json=payload)
                    
                    if response.status_code == 200:
                        res_json = response.json()
                        try:
                            content = res_json["candidates"][0]["content"]["parts"][0]["text"]
                            return content
                        except (KeyError, IndexError) as e:
                            raise Exception(f"Invalid API response format: {json.dumps(res_json)}")
                            
                    elif response.status_code == 429:
                        if attempt < max_retries - 1:
                            logger.warning(f"[{self.name}] Gemini API rate limit exceeded (429). Retrying in {retry_delay}s... (Attempt {attempt + 1}/{max_retries})")
                            await asyncio.sleep(retry_delay)
                            retry_delay *= 2
                            continue
                        else:
                            raise Exception(f"Gemini API returned code 429: {response.text}")
                            
                    else:
                        raise Exception(f"Gemini API returned code {response.status_code}: {response.text}")
            except httpx.RequestError as exc:
                if attempt < max_retries - 1:
                    logger.warning(f"[{self.name}] Network error contacting Gemini API. Retrying in {retry_delay}s... (Attempt {attempt + 1}/{max_retries})")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                else:
                    raise exc

    def clean_json_string(self, raw_str: str) -> str:
        """
        Cleans markdown fences from JSON strings before parsing.
        """
        cleaned = raw_str.strip()
        # Remove markdown wrappers like ```json ... ```
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\n", "", cleaned)
            cleaned = re.sub(r"\n```$", "", cleaned)
        return cleaned.strip()

    async def run(self, project_id: int, context: Dict[str, Any], db_session=None) -> Tuple[Dict[str, Any], str]:
        """
        Executes the agent logic.
        Must be implemented by subclasses.
        Returns: (JSON_output, Markdown_output)
        """
        raise NotImplementedError("Agents must implement run()")
