# University Management REST API

A backend application built with **Python, FastAPI and MySQL** to manage university students, instructors, courses and enrollments.

## Features

- Student management: create, retrieve, list and delete students.
- Instructor management: create and list instructors.
- Course management: create and retrieve courses.
- Enrollment management: register students in courses and retrieve enrollment records.
- Department-based student filtering.
- Retrieve students enrolled in a particular course.
- Retrieve courses taken by a student.
- Retrieve courses taught by an instructor.
- Input validation and duplicate-record handling.
- Relational database design using primary and foreign keys.
- Interactive API documentation through Swagger UI.

## Tech Stack

- Python
- FastAPI
- MySQL
- SQLAlchemy ORM
- Pydantic
- PyMySQL
- Uvicorn

## Database Design

The application uses four relational tables:

| Table | Purpose |
|---|---|
| Students | Stores student information |
| Instructors | Stores instructor information |
| Courses | Stores courses and assigned instructors |
| Enrollments | Connects students with courses |

## Project Structure

```text
university-management-api/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── .gitignore
├── README.md
├── requirements.txt
└── seed.py
```

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/Sunveerkaur22/university-management-api.git
cd university-management-api
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL

Create a MySQL database named `university_db`.

Create a `.env` file in the project root:

```env
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=university_db
```

The application creates its tables using SQLAlchemy when it starts.

### 5. Populate sample data

```bash
python seed.py
```

### 6. Start the API

```bash
python -m uvicorn app.main:app --reload
```

## API Documentation

Once the application is running, visit:

**Swagger UI:** http://127.0.0.1:8000/docs

**ReDoc:** http://127.0.0.1:8000/redoc

## Learning Outcomes

This project demonstrates practical experience with REST API development, Python backend programming, relational database management, SQLAlchemy ORM, request validation, CRUD operations and database relationships.
