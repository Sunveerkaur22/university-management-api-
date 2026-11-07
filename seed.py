
from datetime import date
from app.database import SessionLocal
from app.models import Student, Instructor, Course, Enrollment

db = SessionLocal()

try:
    # 1. Instructors
    instructor_data = [
        ("Dr. Emily Carter", "emily.carter@university.edu"),
        ("Prof. James Wilson", "james.wilson@university.edu"),
        ("Dr. Sophia Martin", "sophia.martin@university.edu"),
        ("Prof. Daniel Brown", "daniel.brown@university.edu"),
        ("Dr. Olivia Taylor", "olivia.taylor@university.edu"),
    ]

    for name, email in instructor_data:
        if not db.query(Instructor).filter_by(email=email).first():
            db.add(Instructor(full_name=name, email=email))

    db.commit()

    # 2. Students
    student_data = [
        ("Aarav Sharma", "aarav@university.edu", "Computer Science"),
        ("Emma Johnson", "emma@university.edu", "Business"),
        ("Noah Williams", "noah@university.edu", "Mathematics"),
        ("Olivia Brown", "olivia@university.edu", "Computer Science"),
        ("Liam Jones", "liam@university.edu", "Engineering"),
        ("Sophia Garcia", "sophia@university.edu", "Business"),
        ("Mason Miller", "mason@university.edu", "Mathematics"),
        ("Isabella Davis", "isabella@university.edu", "Computer Science"),
        ("Ethan Wilson", "ethan@university.edu", "Engineering"),
        ("Mia Anderson", "mia@university.edu", "Business"),
        ("Lucas Thomas", "lucas@university.edu", "Computer Science"),
        ("Amelia Moore", "amelia@university.edu", "Mathematics"),
        ("Benjamin Martin", "benjamin@university.edu", "Engineering"),
        ("Charlotte Lee", "charlotte@university.edu", "Business"),
        ("Henry Perez", "henry@university.edu", "Computer Science"),
        ("Harper Thompson", "harper@university.edu", "Mathematics"),
        ("Alexander White", "alexander@university.edu", "Engineering"),
        ("Evelyn Harris", "evelyn@university.edu", "Business"),
        ("Daniel Clark", "daniel@university.edu", "Computer Science"),
        ("Abigail Lewis", "abigail@university.edu", "Mathematics"),
    ]

    for name, email, department in student_data:
        if not db.query(Student).filter_by(email=email).first():
            db.add(Student(
                full_name=name,
                email=email,
                department=department
            ))

    db.commit()

    # 3. Courses and their instructors
    courses_data = [
        ("Python Programming", "CS101", 4, "emily.carter@university.edu"),
        ("Database Management", "CS102", 4, "james.wilson@university.edu"),
        ("Data Structures", "CS103", 3, "emily.carter@university.edu"),
        ("Business Management", "BUS101", 3, "sophia.martin@university.edu"),
        ("Financial Accounting", "BUS102", 3, "sophia.martin@university.edu"),
        ("Applied Mathematics", "MATH101", 4, "daniel.brown@university.edu"),
        ("Statistics", "MATH102", 3, "daniel.brown@university.edu"),
        ("Engineering Fundamentals", "ENG101", 4, "olivia.taylor@university.edu"),
    ]

    for name, code, credits, instructor_email in courses_data:
        instructor = db.query(Instructor).filter_by(
            email=instructor_email
        ).first()

        if not db.query(Course).filter_by(course_code=code).first():
            db.add(Course(
                course_name=name,
                course_code=code,
                credits=credits,
                instructor_id=instructor.id
            ))

    db.commit()

    # 4. Student-course enrollments
    students = db.query(Student).all()
    courses = db.query(Course).all()

    for student in students:
        matching_courses = [
            course for course in courses
            if course.course_code.startswith(
                {"Computer Science": "CS",
                 "Business": "BUS",
                 "Mathematics": "MATH",
                 "Engineering": "ENG"}.get(student.department, "CS")
            )
        ]

        for course in matching_courses[:2]:
            existing = db.query(Enrollment).filter_by(
                student_id=student.id,
                course_id=course.id
            ).first()

            if not existing:
                db.add(Enrollment(
                    student_id=student.id,
                    course_id=course.id,
                    enrollment_date=date(2026, 9, 1)
                ))

    db.commit()

    print("University database populated successfully!")
    print("Students:", db.query(Student).count())
    print("Instructors:", db.query(Instructor).count())
    print("Courses:", db.query(Course).count())
    print("Enrollments:", db.query(Enrollment).count())

except Exception:
    db.rollback()
    raise

finally:
    db.close()
