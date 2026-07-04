import json
from typing import Dict, Any, Tuple
from app.agents.base import BaseAgent

class DatabaseEngineer(BaseAgent):
    def __init__(self):
        super().__init__("Database Engineer", "Database Architect")

    async def run(self, project_id: int, context: Dict[str, Any], db_session=None) -> Tuple[Dict[str, Any], str]:
        await self.log(project_id, "Formulating database schema...", "INFO", db_session)
        
        arch = context.get("architecture_design", {})
        
        json_out = None
        if self.api_key:
            try:
                await self.log(project_id, "Calling Gemini API to design database schemas...", "INFO", db_session)
                system_instruction = (
                    "You are an expert Database Engineer. Design the tables, column types, and constraints for the project. "
                    "Output ONLY a valid JSON containing: dialect, tables (list of objects with name, description, "
                    "columns (list of objects with name, type, constraints)), indexes (list of objects with table, column, unique)."
                )
                raw_response = await self.call_gemini(system_instruction, json.dumps(arch))
                json_out = json.loads(self.clean_json_string(raw_response))
            except Exception as e:
                await self.log(project_id, f"Gemini API execution failed, falling back to simulated database schema. Detail: {str(e)}", "WARNING", db_session)
                
        if not json_out:
            await self.log(project_id, "Using Mock Fallback mode to build database models.", "INFO", db_session)
            json_out = {
                "dialect": "PostgreSQL / SQLite",
                "tables": [
                    {
                        "name": "users",
                        "description": "System accounts and profiles",
                        "columns": [
                            {"name": "id", "type": "INTEGER", "constraints": "PRIMARY KEY, AUTOINCREMENT"},
                            {"name": "email", "type": "VARCHAR(255)", "constraints": "UNIQUE, INDEX, NOT NULL"},
                            {"name": "hashed_password", "type": "VARCHAR(255)", "constraints": "NOT NULL"},
                            {"name": "full_name", "type": "VARCHAR(100)", "constraints": "NULL"},
                            {"name": "role", "type": "VARCHAR(20)", "constraints": "DEFAULT 'user'"},
                            {"name": "created_at", "type": "TIMESTAMP", "constraints": "DEFAULT CURRENT_TIMESTAMP"}
                        ]
                    },
                    {
                        "name": "records",
                        "description": "Transactional pipeline records",
                        "columns": [
                            {"name": "id", "type": "INTEGER", "constraints": "PRIMARY KEY, AUTOINCREMENT"},
                            {"name": "title", "type": "VARCHAR(100)", "constraints": "NOT NULL"},
                            {"name": "data_payload", "type": "JSON", "constraints": "NULL"},
                            {"name": "status", "type": "VARCHAR(50)", "constraints": "DEFAULT 'draft'"},
                            {"name": "user_id", "type": "INTEGER", "constraints": "FOREIGN KEY REFERENCES users(id) ON DELETE CASCADE"}
                        ]
                    }
                ],
                "indexes": [
                    {"table": "users", "column": "email", "unique": True},
                    {"table": "records", "column": "user_id", "unique": False}
                ]
            }
                
        # Generate Markdown description
        markdown_out = f"""# Database Schema Specification

**Database Dialect:** {json_out.get('dialect', 'N/A')}

"""
        for table in json_out.get('tables', []):
            markdown_out += f"## Table: `{table.get('name')}`\n"
            markdown_out += f"*{table.get('description', '')}*\n\n"
            markdown_out += "| Column Name | Type | Constraints |\n|---|---|---|\n"
            for col in table.get('columns', []):
                markdown_out += f"| `{col.get('name')}` | {col.get('type')} | {col.get('constraints')} |\n"
            markdown_out += "\n"

        markdown_out += "## Indexes and Optimization\n"
        markdown_out += "| Table Name | Column Name | Unique? |\n|---|---|---|\n"
        for idx in json_out.get('indexes', []):
            markdown_out += f"| `{idx.get('table')}` | `{idx.get('column')}` | {'Yes' if idx.get('unique') else 'No'} |\n"

        await self.log(project_id, "Database design finalized.", "SUCCESS", db_session)
        return json_out, markdown_out
