from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.api.deps import get_admin_user
from app.models import User, AuditLog
from app.schemas import AuditLogResponse

router = APIRouter(prefix="/audit", tags=["Audit"])

@router.get("/", response_model=List[AuditLogResponse])
async def list_audit_logs(
    current_admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(AuditLog).order_by(AuditLog.created_at.desc())
    )
    return result.scalars().all()
