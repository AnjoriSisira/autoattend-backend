from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.api import dependencies
from app.db.database import get_db
from app.models.course import Attendance, Session
from app.models.user import User
from app.schemas.schemas import AttendanceResponse

router = APIRouter()

@router.get("/my", response_model=List[AttendanceResponse])
async def get_my_attendance(
    db: AsyncSession = Depends(get_db),
    current_student: User = Depends(dependencies.get_current_active_student)
) -> Any:
    """
    Student viewing their own attendance logs.
    """
    result = await db.execute(select(Attendance).where(Attendance.student_id == current_student.id))
    attendances = result.scalars().all()
    return attendances

@router.get("/course/{course_id}", response_model=List[AttendanceResponse])
async def get_course_attendance(
    course_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_teacher: User = Depends(dependencies.get_current_active_teacher)
) -> Any:
    """
    Teacher viewing logs for a specific class.
    """
    # In a real app, verify the teacher owns this course first.
    # Joining Sessions to get all attendances for the course
    result = await db.execute(
        select(Attendance).join(Session).where(Session.course_id == course_id)
    )
    attendances = result.scalars().all()
    return attendances

@router.post("/mark", response_model=AttendanceResponse)
async def mark_attendance_manual(
    session_id: UUID,
    student_id: UUID,
    status: str,
    db: AsyncSession = Depends(get_db),
    current_teacher: User = Depends(dependencies.get_current_active_teacher)
) -> Any:
    """
    Teacher explicitly marking attendance (fallback manual override).
    """
    new_record = Attendance(
        session_id=session_id,
        student_id=student_id,
        status=status,
        marked_by=str(current_teacher.id),
        confidence_score=1.0 # Manual implies 100% confidence
    )
    db.add(new_record)
    await db.commit()
    await db.refresh(new_record)
    return new_record

from fastapi import UploadFile, File
from app.services.attendance import process_attendance_image

@router.post("/scan", response_model=AttendanceResponse)
async def mark_attendance_via_ml_scan(
    session_id: UUID,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    # Might be invoked by a teacher tablet or a student app, depending on the UX
    current_user: User = Depends(dependencies.get_current_active_user) 
) -> Any:
    """
    System marking attendance via ML face recognition scan.
    Receives an image, processing it against the mock ML engine.
    """
    attendance_record = await process_attendance_image(db, session_id, file)
    return attendance_record
