import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from sqlalchemy import func
from sqlalchemy.orm import Session
import models
import schemas


def create_student(db: Session, data: schemas.StudentCreate):
    class_obj = get_class_by_id(db, data.class_id)
    if not class_obj:
        raise LookupError("Class not found")

    student = models.Student(**data.model_dump())
    db.add(student)
    db.flush()

    class_obj.no_of_students = get_student_count_by_class_id(db, data.class_id)

    db.commit()
    db.refresh(student)
    db.refresh(class_obj)
    return student


def get_student_by_rollno(db: Session, rollno: str):
    return (
        db.query(models.Student).filter(models.Student.student_rollno == rollno).first()
    )


def get_all_students(db: Session):
    return db.query(models.Student).all()


def update_student(db: Session, rollno: str, updated_data: schemas.StudentUpdate):
    return _update_student(db, rollno, updated_data)


def _update_student(db: Session, rollno: str, updated_data):
    student = get_student_by_rollno(db, rollno)
    if not student:
        raise LookupError("Student not found")

    old_class_id = student.class_id
    new_class_id = updated_data.class_id

    new_class_obj = get_class_by_id(db, new_class_id)
    if not new_class_obj:
        raise LookupError("Class not found")

    for key, value in updated_data.model_dump().items():
        setattr(student, key, value)

    db.flush()

    affected_class_ids = {old_class_id, new_class_id}
    for class_id in affected_class_ids:
        class_obj = get_class_by_id(db, class_id)
        if class_obj:
            class_obj.no_of_students = get_student_count_by_class_id(db, class_id)

    db.commit()
    db.refresh(student)
    return student


def delete_student(db: Session, rollno: str):
    student = get_student_by_rollno(db, rollno)
    if not student:
        raise LookupError("Student not found")

    class_id = student.class_id
    db.delete(student)
    db.flush()

    class_obj = get_class_by_id(db, class_id)
    if class_obj:
        class_obj.no_of_students = get_student_count_by_class_id(db, class_id)

    db.commit()
    return {"detail": "Student deleted successfully"}


def get_student_count_by_class_id(db: Session, class_id: int) -> int:
    return (
        db.query(func.count(models.Student.id))
        .filter(models.Student.class_id == class_id)
        .scalar()
    )


def create_class(db: Session, data: schemas.ClassCreate):
    class_obj = models.Class(
        grade=data.grade,
        section=data.section,
        school_name=data.school_name,
        no_of_students=0,
    )
    db.add(class_obj)
    db.commit()
    db.refresh(class_obj)
    return class_obj


def get_class_by_id(db: Session, class_id: int):
    return db.query(models.Class).filter(models.Class.id == class_id).first()


def get_all_classes(db: Session):
    return db.query(models.Class).all()


def update_class(db: Session, class_id: int, updated_data: schemas.ClassCreate):
    class_obj = get_class_by_id(db, class_id)
    if not class_obj:
        raise LookupError("Class not found")
    for key, value in updated_data.model_dump().items():
        setattr(class_obj, key, value)
    db.commit()
    db.refresh(class_obj)
    return class_obj


def delete_class(db: Session, class_id: int):
    class_obj = get_class_by_id(db, class_id)
    if not class_obj:
        raise LookupError("Class not found")
    if get_student_count_by_class_id(db, class_id) > 0:
        raise ValueError("Cannot delete a class that still has students")
    db.delete(class_obj)
    db.commit()
    return {"detail": "Class deleted successfully"}


def insert_top_score(db: Session, min_score: int):
    if not 70 < min_score <= 100:
        return

    try:
        db.query(models.TopperStudent).delete(synchronize_session=False)
        students = (
            db.query(models.Student, models.Class.grade, models.Class.section)
            .join(models.Class, models.Student.class_id == models.Class.id)
            .filter(models.Student.student_score >= min_score)
            .all()
        )

        for student, grade, section in students:
            topper_data = models.TopperStudent(
                student_name=student.student_name,
                student_rollno=student.student_rollno,
                student_score=student.student_score,
                grade=grade,
                section=section,
            )
            db.add(topper_data)

        db.commit()
    except Exception:
        db.rollback()
        raise


def get_toppers_with_school_name(db: Session):
    results = (
        db.query(models.TopperStudent, models.Class.school_name)
        .join(
            models.Student,
            models.TopperStudent.student_rollno == models.Student.student_rollno,
        )
        .join(models.Class, models.Student.class_id == models.Class.id)
        .all()
    )

    return [
        schemas.TopperStudentOut(
            student_name=student.student_name,
            student_rollno=student.student_rollno,
            grade=student.grade,
            section=student.section,
            student_score=student.student_score,
            school_name=school_name,
        )
        for student, school_name in results
    ]
