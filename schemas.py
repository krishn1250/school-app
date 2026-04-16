from pydantic import BaseModel, ConfigDict


class StudentBaseModel(BaseModel):
    student_name: str
    student_rollno: str
    student_score: float
    class_id: int


class StudentCreate(StudentBaseModel):
    pass


class StudentUpdate(BaseModel):
    student_name: str
    student_score: float
    class_id: int


class StudentRead(StudentBaseModel):
    student_rollno: str
    model_config = ConfigDict(from_attributes=True)


class ClassBase(BaseModel):
    grade: str
    section: str
    school_name: str


class ClassCreate(ClassBase):
    pass


class ClassOut(ClassBase):
    id: int
    no_of_students: int
    model_config = ConfigDict(from_attributes=True)


class TopperStudentOut(BaseModel):
    student_name: str
    student_rollno: str
    grade: str
    section: str
    student_score: float
    school_name: str
