import random
from datetime import date, datetime, timedelta
from faker import Faker
from database import Session
from models import Student, Group, Teacher, Subject, Grade

fake = Faker()

def create_groups():
    groups = []
    group_names = ['ІТ-101', 'ІТ-102', 'ІТ-103']
    
    for name in group_names:
        group = Group(
            name=name,
            description=f"Група {name} для вивчення інформаційних технологій"
        )
        groups.append(group)
    
    return groups

def create_teachers():
    teachers = []
    
    for _ in range(random.randint(3, 5)):
        teacher = Teacher(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.unique.email(),
            phone=fake.phone_number()[:19]
        )
        teachers.append(teacher)
    
    return teachers

def create_subjects(teachers):
    subjects = []
    subject_names = [
        'Математика', 'Фізика', 'Програмування', 'Бази даних', 
        'Веб-розробка', 'Алгоритми', 'Операційні системи', 'Мережі'
    ]
    
    selected_subjects = random.sample(subject_names, random.randint(5, 8))
    
    for subject_name in selected_subjects:
        subject = Subject(
            name=subject_name,
            description=f"Курс з {subject_name.lower()}",
            credits=random.randint(1, 6),
            teacher_id=random.choice(teachers).id
        )
        subjects.append(subject)
    
    return subjects

def create_students(groups):
    students = []
    
    for _ in range(random.randint(30, 50)):
        student = Student(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.unique.email(),
            birth_date=fake.date_of_birth(minimum_age=18, maximum_age=25),
            group_id=random.choice(groups).id
        )
        students.append(student)
    
    return students

def create_grades(students, subjects):
    grades = []
    
    for student in students:
        for subject in subjects:
            num_grades = random.randint(1, 20)
            
            for _ in range(num_grades):
                grade = Grade(
                    score=random.randint(60, 100),
                    grade_date=fake.date_between(start_date='-1y', end_date='today'),
                    created_at=datetime.now(),
                    student_id=student.id,
                    subject_id=subject.id
                )
                grades.append(grade)
    
    return grades

def seed_database():
    session = Session()
    
    try:
        session.query(Grade).delete()
        session.query(Subject).delete()
        session.query(Student).delete()
        session.query(Teacher).delete()
        session.query(Group).delete()
        session.commit()
        
        print("Створюємо групи...")
        groups = create_groups()
        session.add_all(groups)
        session.commit()
        
        print("Створюємо викладачів...")
        teachers = create_teachers()
        session.add_all(teachers)
        session.commit()
        
        print("Створюємо предмети...")
        subjects = create_subjects(teachers)
        session.add_all(subjects)
        session.commit()
        
        print("Створюємо студентів...")
        students = create_students(groups)
        session.add_all(students)
        session.commit()
        
        print("Створюємо оцінки...")
        grades = create_grades(students, subjects)
        session.add_all(grades)
        session.commit()
        
        print(f"База даних заповнена!")
        print(f"Створено: {len(groups)} груп, {len(teachers)} викладачів, {len(subjects)} предметів")
        print(f"Створено: {len(students)} студентів, {len(grades)} оцінок")
        
    except Exception as e:
        session.rollback()
        print(f"Помилка: {e}")
    
    finally:
        session.close()

if __name__ == "__main__":
    seed_database() 