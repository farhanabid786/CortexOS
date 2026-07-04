from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.api.deps import get_current_active_user
from app.models import User, Blueprint, Project
from app.schemas import BlueprintResponse

router = APIRouter(prefix="/blueprints", tags=["Blueprints"])

@router.get("/{project_id}", response_model=BlueprintResponse)
async def get_blueprint(
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
        select(Blueprint).filter(Blueprint.project_id == project_id)
    )
    blueprint = result.scalars().first()
    if not blueprint:
        raise HTTPException(
            status_code=404, 
            detail="Blueprint not generated yet. Verify project orchestration pipeline is complete."
        )
    return blueprint
