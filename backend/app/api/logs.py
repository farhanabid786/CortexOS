from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.api.deps import get_current_active_user
from app.models import User, AgentLog, Project
from app.schemas import AgentLogResponse

router = APIRouter(prefix="/logs", tags=["Logs"])

@router.get("/{project_id}", response_model=List[AgentLogResponse])
async def get_agent_logs(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    # Verify project belongs to current user
    proj_result = await db.execute(
        select(Project).filter(Project.id == project_id, Project.user_id == current_user.id)
    )
    project = proj_result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    result = await db.execute(
        select(AgentLog).filter(AgentLog.project_id == project_id).order_by(AgentLog.created_at.asc())
    )
    return result.scalars().all()
