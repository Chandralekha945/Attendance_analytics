from datetime import datetime, timezone, timedelta
from typing import Optional

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Query

from app.database import attendance_collection, employees_collection
from app.models import EmployeeCreate, AttendanceCorrection

router = APIRouter(prefix="/attendance", tags=["Attendance"])


def utc_now():
    return datetime.now(timezone.utc)


def get_today():
    return utc_now().date().isoformat()


@router.post("/employees", status_code=201)
def create_employee(employee: EmployeeCreate):
    existing = employees_collection.find_one({
        "$or": [
            {"employee_id": employee.employee_id},
            {"email": employee.email}
        ]
    })

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Employee ID or email already exists"
        )

    employees_collection.insert_one(employee.model_dump())

    return {
        "message": "Employee registered successfully",
        "employee_id": employee.employee_id
    }


@router.post("/punch-in")
def punch_in(employee_id: str):
    employee = employees_collection.find_one({
        "employee_id": employee_id
    })

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    today = get_today()

    existing = attendance_collection.find_one({
        "employee_id": employee_id,
        "date": today
    })

    if existing and existing.get("punch_in"):
        raise HTTPException(
            status_code=409,
            detail="Employee has already punched in today"
        )

    now = utc_now()

    if existing:
        attendance_collection.update_one(
            {"_id": existing["_id"]},
            {"$set": {"punch_in": now, "status": "Present"}}
        )
    else:
        attendance_collection.insert_one({
            "employee_id": employee_id,
            "date": today,
            "punch_in": now,
            "punch_out": None,
            "status": "Present"
        })

    return {
        "message": "Punch-in recorded successfully",
        "employee_id": employee_id,
        "punch_in": now.isoformat()
    }


@router.post("/punch-out")
def punch_out(employee_id: str):
    today = get_today()

    record = attendance_collection.find_one({
        "employee_id": employee_id,
        "date": today
    })

    if not record:
        raise HTTPException(
            status_code=404,
            detail="No attendance record found. Punch in first."
        )

    if not record.get("punch_in"):
        raise HTTPException(
            status_code=400,
            detail="Punch in before punching out"
        )

    if record.get("punch_out"):
        raise HTTPException(
            status_code=409,
            detail="Employee has already punched out today"
        )

    now = utc_now()

    attendance_collection.update_one(
        {"_id": record["_id"]},
        {"$set": {"punch_out": now}}
    )

    return {
        "message": "Punch-out recorded successfully",
        "employee_id": employee_id,
        "punch_out": now.isoformat()
    }


@router.get("/{employee_id}")
def get_attendance(
    employee_id: str,
    start_date: Optional[str] = Query(default=None),
    end_date: Optional[str] = Query(default=None)
):
    query = {"employee_id": employee_id}

    if start_date or end_date:
        date_filter = {}

        if start_date:
            date_filter["$gte"] = start_date

        if end_date:
            date_filter["$lte"] = end_date

        query["date"] = date_filter

    records = list(
        attendance_collection.find(query).sort("date", -1)
    )

    for record in records:
        record["_id"] = str(record["_id"])

        for field in ("punch_in", "punch_out"):
            if record.get(field):
                record[field] = record[field].isoformat()

    return {
        "employee_id": employee_id,
        "count": len(records),
        "records": records
    }


@router.patch("/{record_id}/correct")
def correct_attendance(
    record_id: str,
    correction: AttendanceCorrection
):
    if not ObjectId.is_valid(record_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid attendance record ID"
        )

    updates = {}

    if correction.punch_in is not None:
        try:
            updates["punch_in"] = datetime.fromisoformat(
                correction.punch_in.replace("Z", "+00:00")
            )
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid punch-in datetime"
            )

    if correction.punch_out is not None:
        try:
            updates["punch_out"] = datetime.fromisoformat(
                correction.punch_out.replace("Z", "+00:00")
            )
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid punch-out datetime"
            )

    if not updates:
        raise HTTPException(
            status_code=400,
            detail="Provide at least one attendance field to correct"
        )

    record = attendance_collection.find_one({
        "_id": ObjectId(record_id)
    })

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Attendance record not found"
        )

    punch_in = updates.get("punch_in", record.get("punch_in"))
    punch_out = updates.get("punch_out", record.get("punch_out"))

    if punch_in and punch_out and punch_out < punch_in:
        raise HTTPException(
            status_code=400,
            detail="Punch-out cannot be earlier than punch-in"
        )

    updates["correction_reason"] = correction.reason
    updates["corrected_at"] = utc_now()

    attendance_collection.update_one(
        {"_id": ObjectId(record_id)},
        {"$set": updates}
    )

    return {
        "message": "Attendance corrected successfully",
        "record_id": record_id,
        "reason": correction.reason
    }