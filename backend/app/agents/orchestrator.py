import asyncio
import logging
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session
from app.models import Project, Blueprint, AgentLog
from app.agents.requirement_analyst import RequirementAnalyst
from app.agents.product_manager import ProductManager
from app.agents.software_architect import SoftwareArchitect
from app.agents.database_engineer import DatabaseEngineer
from app.agents.backend_engineer import BackendEngineer
from app.agents.frontend_engineer import FrontendEngineer
from app.agents.qa_engineer import QAEngineer
from app.agents.security_analyst import SecurityAnalyst
from app.agents.documentation_agent import DocumentationAgent
from app.agents.review_agent import ReviewAgent

logger = logging.getLogger("cortexos.orchestrator")

class CortexOrchestrator:
    def __init__(self):
        self.agents = [
            RequirementAnalyst(),
            ProductManager(),
            SoftwareArchitect(),
            DatabaseEngineer(),
            BackendEngineer(),
            FrontendEngineer(),
            QAEngineer(),
            SecurityAnalyst(),
            DocumentationAgent(),
            ReviewAgent()
        ]

    async def run_pipeline(self, project_id: int):
        """
        Executes the 10-agent pipeline sequentially in the background.
        """
        logger.info(f"Orchestrator starting pipeline for project {project_id}")
        
        async with async_session() as session:
            # 1. Fetch project
            result = await session.execute(select(Project).filter(Project.id == project_id))
            project = result.scalars().first()
            if not project:
                logger.error(f"Project {project_id} not found in database.")
                return
                
            project.status = "running"
            await session.commit()
            
            # Clear old logs if any
            from sqlalchemy import delete
            await session.execute(delete(AgentLog).where(AgentLog.project_id == project_id))
            await session.commit()
            
        context = {
            "project_id": project_id,
            "title": project.title,
            "description": project.description,
            "prompt": project.prompt
        }
        
        compiled_markdowns = []
        blueprint_data = {}
        
        try:
            for agent in self.agents:
                # Update current running agent in DB
                async with async_session() as session:
                    db_project = await session.get(Project, project_id)
                    if db_project:
                        db_project.current_agent = agent.name
                        await session.commit()
                
                # Execute agent
                # We reopen session for each agent to write log entries dynamically
                async with async_session() as agent_session:
                    json_out, md_out = await agent.run(project_id, context, db_session=agent_session)
                    
                # Store output in orchestrator context for subsequent downstream agents
                snake_name = agent.name.lower().replace(" ", "_")
                context[snake_name] = json_out
                blueprint_data[snake_name] = json_out
                compiled_markdowns.append(md_out)
                
                # Small pause to allow frontend log subscription animation to flow nicely
                await asyncio.sleep(0.5)

            # 2. Pipeline Successful: Save blueprint and update project status
            async with async_session() as final_session:
                db_project = await final_session.get(Project, project_id)
                if db_project:
                    db_project.status = "completed"
                    db_project.current_agent = None
                    
                    # Check if blueprint already exists, or create a new one
                    bp_result = await final_session.execute(
                        select(Blueprint).filter(Blueprint.project_id == project_id)
                    )
                    blueprint = bp_result.scalars().first()
                    if not blueprint:
                        blueprint = Blueprint(project_id=project_id)
                        final_session.add(blueprint)
                        
                    blueprint.requirement_analysis = blueprint_data.get("requirement_analyst")
                    blueprint.prd = blueprint_data.get("product_manager")
                    blueprint.architecture_design = blueprint_data.get("software_architect")
                    blueprint.database_schema = blueprint_data.get("database_engineer")
                    blueprint.api_design = blueprint_data.get("backend_engineer")
                    blueprint.frontend_plan = blueprint_data.get("frontend_engineer")
                    blueprint.testing_strategy = blueprint_data.get("qa_engineer")
                    blueprint.security_report = blueprint_data.get("security_analyst")
                    blueprint.deployment_guide = blueprint_data.get("documentation_agent")
                    blueprint.review_report = blueprint_data.get("review_agent")
                    
                    # Combine all generated markdown
                    blueprint.markdown_output = "\n\n***\n\n".join(compiled_markdowns)
                    
                    await final_session.commit()
                    logger.info(f"Orchestrator successfully generated blueprint for project {project_id}")
                    
        except Exception as e:
            logger.exception(f"Orchestration pipeline failed for project {project_id}: {str(e)}")
            async with async_session() as fail_session:
                db_project = await fail_session.get(Project, project_id)
                if db_project:
                    db_project.status = "failed"
                    db_project.current_agent = None
                    
                    # Log error to agent logs
                    err_log = AgentLog(
                        project_id=project_id,
                        agent_name="Cortex Orchestrator",
                        log_level="ERROR",
                        message=f"Pipeline execution halted due to failure: {str(e)}"
                    )
                    fail_session.add(err_log)
                    await fail_session.commit()

# Single global orchestrator instance
orchestrator = CortexOrchestrator()
