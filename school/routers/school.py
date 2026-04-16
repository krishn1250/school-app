import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas
from school.crud import crud
from database import get_db

router = APIRouter(prefix="/school", tags=["School CRUD"])
# router=APIRouter(
#     prefix="/school",
#     tags=["class CRUD"]
# )


@router.post("/students/", response_model=schemas.StudentRead)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = crud.get_student_by_rollno(db, student.student_rollno)
    if db_student:
        raise HTTPException(
            status_code=400, detail="Student with this roll number already exists"
        )
    try:
        return crud.create_student(db, student)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/students/{rollno}", response_model=schemas.StudentRead)
def read_student(rollno: str, db: Session = Depends(get_db)):
    db_student = crud.get_student_by_rollno(db, rollno)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@router.get("/students/", response_model=list[schemas.StudentRead])
def read_all_students(db: Session = Depends(get_db)):
    return crud.get_all_students(db)


@router.put("/students/{rollno}", response_model=schemas.StudentRead)
def update_student(
    rollno: str, student: schemas.StudentUpdate, db: Session = Depends(get_db)
):
    try:
        return crud.update_student(db, rollno, student)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.delete("/students/{rollno}")
def delete_student(rollno: str, db: Session = Depends(get_db)):
    try:
        return crud.delete_student(db, rollno)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/classes/", response_model=schemas.ClassOut)
def create_class(class_data: schemas.ClassCreate, db: Session = Depends(get_db)):
    return crud.create_class(db, class_data)


@router.get("/classes/{class_id}", response_model=schemas.ClassOut)
def read_class(class_id: int, db: Session = Depends(get_db)):
    class_obj = crud.get_class_by_id(db, class_id)
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_obj


@router.get("/classes/", response_model=list[schemas.ClassOut])
def read_all_classes(db: Session = Depends(get_db)):
    return crud.get_all_classes(db)


@router.put("/classes/{class_id}", response_model=schemas.ClassOut)
def update_class(
    class_id: int, class_data: schemas.ClassCreate, db: Session = Depends(get_db)
):
    try:
        return crud.update_class(db, class_id, class_data)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.delete("/classes/{class_id}")
def delete_class(class_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_class(db, class_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
