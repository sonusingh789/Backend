from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Student(BaseModel):
    id: int
    name: str
    age: int
    course: str


students = []


@app.get("/")
def home():
    return {"Message ": "Welcome to Student API"}


@app.post("/student")
def add_student(student: Student):
    students.append(student)
    return {"Message": "Student Added Sucessfully", "Student": student}


@app.get("/student/{student_id}")
def get_student(student_id: int):
    for student in students:
        if student.id == student_id:
            return student

    return {"message": "Student not Found "}


@app.delete("/student/{student_id}")
def delete_student(student_id: int):
    for student in students:
        if student.id == student_id:
            students.remove(student)

            return {"Message": "Student Deleted Successfully", "Student": student}

    return {"message": "Student not Found"}


@app.put("/student/{student_id}")
def update_student(student_id: int, updated_student: Student):
    for i in range(len(students)):
        if students[i].id == student_id:
            students[i] = updated_student

            return {
                "Message": "Student Updated Successfully",
                "Student": updated_student,
            }

    return {"message": "Student not Found"}
