
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import date


# STUDENTS
class StudentCreate(BaseModel):
    full_name: str
    email: EmailStr
    department: Optional[str] = None


class StudentResponse(BaseModel):
    id: int
    full_name: str
    email: str
    department: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# INSTRUCTORS
class InstructorCreate(BaseModel):
    full_name: str
    email: EmailStr


class InstructorResponse(BaseModel):
    id: int
    full_name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


# COURSES
class CourseCreate(BaseModel):
    course_name: str
    course_code: str
    credits: int
    instructor_id: int


class CourseResponse(BaseModel):
    id: int
    course_name: str
    course_code: str
    credits: int
    instructor_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


# ENROLLMENTS
class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int
    enrollment_date: date


class EnrollmentResponse(BaseModel):
    student_id: int
    course_id: int
    enrollment_date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)

