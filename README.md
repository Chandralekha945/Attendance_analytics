# Employee Attendance & Analytics API

A REST API for employee attendance management and analytics built using
Python, FastAPI, and MongoDB.

## Features

- Register employees
- Record attendance punch-in and punch-out
- Retrieve employee attendance records
- Correct attendance records with a reason
- Generate employee attendance summaries
- Generate daily attendance analytics
- Interactive API documentation using Swagger UI

## Technologies

- Python 3.11+
- FastAPI
- MongoDB
- PyMongo
- Uvicorn

## Project Structure

```text
attendance-analytics-api/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── routes/
│   │   ├── attendance.py
│   │   └── analytics.py
│   └── services/
│       └── analytics_service.py
├── requirements.txt
├── README.md
├── REVIEW.md
├── DECISIONS.md
└── .gitignore