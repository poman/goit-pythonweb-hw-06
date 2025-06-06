from datetime import datetime, date
from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    DateTime,
    Date,
)
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    mapped_column,
    Mapped,
)

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100))
    birth_date: Mapped[date] = mapped_column(Date)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    
    # Relationships
    group: Mapped["Group"] = relationship("Group", back_populates="students")
    grades: Mapped[list["Grade"]] = relationship("Grade", back_populates="student")
    
    def __repr__(self) -> str:
        return f"<Student(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}')>"

class Group(Base):
    __tablename__ = "groups"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(200))
    
    # Relationships
    students: Mapped[list["Student"]] = relationship("Student", back_populates="group")

    def __repr__(self) -> str:
        return f"<Group(id={self.id}, name='{self.name}')>"

class Teacher(Base):
    __tablename__ = "teachers"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(20))
    
    # Relationships
    subjects: Mapped[list["Subject"]] = relationship("Subject", back_populates="teacher")

    def __repr__(self) -> str:
        return f"<Teacher(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}')>"

class Subject(Base):
    __tablename__ = "subjects"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500))
    credits: Mapped[int] = mapped_column(Integer)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id", ondelete="CASCADE"))
    
    # Relationships
    teacher: Mapped["Teacher"] = relationship("Teacher", back_populates="subjects")
    grades: Mapped[list["Grade"]] = relationship("Grade", back_populates="subject", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Subject(id={self.id}, name='{self.name}')>"
    
class Grade(Base):
    __tablename__ = "grades"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    score: Mapped[int] = mapped_column(Integer)
    grade_date: Mapped[date] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    student_id: Mapped[int] = mapped_column(ForeignKey('students.id'))
    subject_id: Mapped[int] = mapped_column(ForeignKey('subjects.id'))
    
    # Relationships
    student: Mapped["Student"] = relationship("Student", back_populates="grades")
    subject: Mapped["Subject"] = relationship("Subject", back_populates="grades")

    def __repr__(self) -> str:
        return f"<Grade(id={self.id}, score={self.score})>" 
    