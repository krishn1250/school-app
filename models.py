import os
import sys

PROJECT_ROOT = os.path.dirname(__file__)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String, nullable=False)
    student_rollno = Column(String, nullable=False, unique=True)
    student_score = Column(Float, nullable=False)

    class_id = Column(Integer, ForeignKey("class.id"), nullable=False)

    class_ = relationship("Class", back_populates="students")


class Class(Base):
    __tablename__ = "class"

    id = Column(Integer, primary_key=True, index=True)
    grade = Column(String, nullable=False)
    section = Column(String, nullable=False)
    no_of_students = Column(Integer, nullable=False)
    school_name = Column(String, nullable=False)

    students = relationship("Student", back_populates="class_")


class TopperStudent(Base):
    __tablename__ = "topper_students"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String, nullable=False)
    student_rollno = Column(String, nullable=False)
    grade = Column(String, nullable=False)
    section = Column(String, nullable=False)
    student_score = Column(Float, nullable=False)
