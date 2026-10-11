from fastapi import APIRouter

from app.services.analytics_service import (
    get_employee_attendance_summary,
    get_attendance_overview
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/employee/{employee_id}")
def employee_analytics(employee_id: str):
    return get_employee_attendance_summary(employee_id)


@router.get("/overview")
def attendance_overview():
    return {
        "daily_summary": get_attendance_overview()
    }