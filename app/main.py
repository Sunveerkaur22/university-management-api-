from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import engine, Base, get_db
from app.models import Student, Instructor, Course, Enrollment
from app.schemas import (
    StudentCreate, StudentResponse,
    InstructorCreate, InstructorResponse,
    CourseCreate, CourseResponse,
    EnrollmentCreate, EnrollmentResponse
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="University Management API",
    description="REST API for managing university students, instructors, courses and enrollments",
    version="1.0.0"
)


@app.get("/")
def home():
    return {"message": "University Management API is running!"}


# ---------------- STUDENTS ----------------

@app.get("/students", response_model=list[StudentResponse])
def get_students(
    department: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Student)

    if department:
        query = query.filter(Student.department == department)

    return query.all()


@app.post("/students", response_model=StudentResponse, status_code=201)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Student).filter(
        Student.email == student.email
    ).first()

    if existing:
        raise HTTPException(status_code=409, detail="Email already exists")

    new_student = Student(**student.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Remove related enrollments first to respect foreign keys
    db.query(Enrollment).filter(
        Enrollment.student_id == student_id
    ).delete(synchronize_session=False)

    db.delete(student)
    db.commit()

    return {"message": "Student deleted successfully"}


# ---------------- INSTRUCTORS ----------------

@app.get("/instructors", response_model=list[InstructorResponse])
def get_instructors(db: Session = Depends(get_db)):
    return db.query(Instructor).all()


@app.post("/instructors", response_model=InstructorResponse, status_code=201)
def create_instructor(
    instructor: InstructorCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Instructor).filter(
        Instructor.email == instructor.email
    ).first()

    if existing:
        raise HTTPException(status_code=409, detail="Instructor email already exists")

    new_instructor = Instructor(**instructor.model_dump())
    db.add(new_instructor)
    db.commit()
    db.refresh(new_instructor)

    return new_instructor


# ---------------- COURSES ----------------

@app.get("/courses", response_model=list[CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()


@app.post("/courses", response_model=CourseResponse, status_code=201)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db)
):
    if course.credits <= 0:
        raise HTTPException(
            status_code=400,
            detail="Course credits must be greater than zero"
        )

    existing = db.query(Course).filter(
        Course.course_code == course.course_code
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Course code already exists"
        )

    instructor = db.query(Instructor).filter(
        Instructor.id == course.instructor_id
    ).first()

    if not instructor:
        raise HTTPException(
            status_code=404,
            detail="Instructor not found"
        )

    new_course = Course(**course.model_dump())
    db.add(new_course)

    try:
        db.commit()
        db.refresh(new_course)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Could not create course because of a database constraint"
        )

    return new_course


@app.get("/courses/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return course


# ---------------- ENROLLMENTS ----------------

@app.get("/enrollments", response_model=list[EnrollmentResponse])
def get_enrollments(db: Session = Depends(get_db)):
    return db.query(Enrollment).all()


@app.post("/enrollments", response_model=EnrollmentResponse, status_code=201)
def create_enrollment(
    enrollment: EnrollmentCreate,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == enrollment.student_id
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    course = db.query(Course).filter(
        Course.id == enrollment.course_id
    ).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    existing = db.query(Enrollment).filter_by(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id
    ).first()

    if existing:
        raise HTTPException(status_code=409, detail="Student already enrolled in this course")

    new_enrollment = Enrollment(**enrollment.model_dump())
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)

    return new_enrollment


# ---------------- UNIVERSITY RELATIONSHIPS ----------------

@app.get("/courses/{course_id}/students",
         response_model=list[StudentResponse])
def get_course_students(
    course_id: int,
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return (
        db.query(Student)
        .join(Enrollment, Student.id == Enrollment.student_id)
        .filter(Enrollment.course_id == course_id)
        .all()
    )


@app.get("/students/{student_id}/courses",
         response_model=list[CourseResponse])
def get_student_courses(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return (
        db.query(Course)
        .join(Enrollment, Course.id == Enrollment.course_id)
        .filter(Enrollment.student_id == student_id)
        .all()
    )


@app.get("/instructors/{instructor_id}/courses",
         response_model=list[CourseResponse])
def get_instructor_courses(
    instructor_id: int,
    db: Session = Depends(get_db)
):
    instructor = db.query(Instructor).filter(
        Instructor.id == instructor_id
    ).first()

    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")

    return db.query(Course).filter(
        Course.instructor_id == instructor_id
    ).all()
