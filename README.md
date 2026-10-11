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
## MongoDB Setup

This project uses MongoDB to store employee and attendance records.

1. Install MongoDB Community Server.
2. Start the MongoDB service.
3. Create a `.env` file in the project root.
4. Add the following configuration:

   MONGO_URL=mongodb://localhost:27017/

5. Install dependencies:

   pip install -r requirements.txt

6. Start the API:

   python -m uvicorn app.main:app --reload

7. Open the API documentation at:

   http://127.0.0.1:8000/docs