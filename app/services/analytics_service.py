from app.database import attendance_collection


def get_employee_attendance_summary(employee_id: str):
    pipeline = [
        {
            "$match": {
                "employee_id": employee_id
            }
        },
        {
            "$group": {
                "_id": "$employee_id",
                "total_days": {"$sum": 1},
                "present_days": {
                    "$sum": {
                        "$cond": [
                            {"$eq": ["$status", "Present"]},
                            1,
                            0
                        ]
                    }
                },
                "completed_days": {
                    "$sum": {
                        "$cond": [
                            {
                                "$and": [
                                    {"$ne": ["$punch_in", None]},
                                    {"$ne": ["$punch_out", None]}
                                ]
                            },
                            1,
                            0
                        ]
                    }
                }
            }
        }
    ]

    result = list(attendance_collection.aggregate(pipeline))

    if not result:
        return {
            "employee_id": employee_id,
            "total_days": 0,
            "present_days": 0,
            "completed_days": 0
        }

    summary = result[0]

    return {
        "employee_id": employee_id,
        "total_days": summary["total_days"],
        "present_days": summary["present_days"],
        "completed_days": summary["completed_days"]
    }


def get_attendance_overview():
    pipeline = [
        {
            "$group": {
                "_id": "$date",
                "total_records": {"$sum": 1},
                "present_count": {
                    "$sum": {
                        "$cond": [
                            {"$eq": ["$status", "Present"]},
                            1,
                            0
                        ]
                    }
                }
            }
        },
        {
            "$sort": {"_id": -1}
        }
    ]

    results = list(attendance_collection.aggregate(pipeline))

    return [
        {
            "date": result["_id"],
            "total_records": result["total_records"],
            "present_count": result["present_count"]
        }
        for result in results
    ]