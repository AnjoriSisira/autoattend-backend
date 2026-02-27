from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api import dependencies
from app.db.database import get_db
from app.models.course import Session, Course
from app.models.user import User, UserRole
from app.schemas.schemas import SessionResponse

router = APIRouter()

@router.get("/", response_model=List[SessionResponse])
async def get_timetable(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(dependencies.get_current_active_user)
) -> Any:
    """
    Retrieves the timetable for the current user's role.
    """
    if current_user.role == UserRole.TEACHER:
        # Teacher's timetable: Sessions for courses they teach
        result = await db.execute(
            select(Session).join(Course).where(Course.teacher_id == current_user.id)
        )
        sessions = result.scalars().all()
        return sessions
    else:
        # For students/parents, we might return all active sessions or
        # sessions they are enrolled in (requires an Enrollment table).
        # For simplicity, returning all sessions currently.
        result = await db.execute(select(Session))
        sessions = result.scalars().all()
        return sessions
