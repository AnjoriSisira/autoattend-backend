from fastapi import APIRouter
from app.api.v1 import auth, users, attendance, timetable

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
api_router.include_router(timetable.router, prefix="/timetable", tags=["timetable"])
