from fastapi import FastAPI, HTTPException

from app.database import check_database_connection
from app.routes.attendance import router as attendance_router
from app.routes.analytics import router as analytics_router

app = FastAPI(
    title="Employee Attendance & Analytics API",
    description="Employee attendance management and analytics",
    version="1.0.0"
)

app.include_router(attendance_router)
app.include_router(analytics_router)


app.include_router(attendance_router)


@app.get("/")
def home():
    return {
        "message": "Employee Attendance & Analytics API is running!"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/health/database")
def database_health_check():
    if check_database_connection():
        return {
            "status": "connected",
            "database": "attendance_db"
        }

    raise HTTPException(
        status_code=503,
        detail="MongoDB connection failed"
    )