
# University Management API

A RESTful backend application for managing university students, instructors, courses, and enrollments.

## Technologies
- Python
- FastAPI
- MySQL
- SQLAlchemy
- Pydantic
- Uvicorn

## Features
- Student CRUD operations
- Instructor management
- Course management
- Student course enrollment
- Department-based student filtering
- Retrieve students enrolled in a course
- Retrieve courses taken by a student
- Retrieve courses taught by an instructor
- Duplicate record validation
- Relational database with primary and foreign keys
- Interactive API documentation with Swagger UI

## Database Structure

- Students
- Instructors
- Courses
- Enrollments

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd university-management-API
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure your `.env` file:

```env
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=university_db
```

Create the database and tables using the provided SQL setup instructions, then populate sample data:

```bash
python seed.py
```

Start the application:

```bash
python -m uvicorn app.main:app --reload
```

Open API documentation:

http://127.0.0.1:8000/docs

## Project Purpose

This project demonstrates backend development, REST API design, relational database management, SQLAlchemy ORM, and data validation.
