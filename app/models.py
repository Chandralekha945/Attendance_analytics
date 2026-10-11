from pydantic import BaseModel, Field
from typing import Optional


class EmployeeCreate(BaseModel):
    employee_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    email: str


class PunchInRequest(BaseModel):
    employee_id: str


class PunchOutRequest(BaseModel):
    employee_id: str


class AttendanceCorrection(BaseModel):
    punch_in: Optional[str] = None
    punch_out: Optional[str] = None
    reason: str = Field(..., min_length=3)