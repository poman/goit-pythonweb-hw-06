from sqlalchemy import func, desc, and_
from database import Session
from models import Student, Group, Teacher, Subject, Grade


def select_1():
    session = Session()
    try:
        result = session.query(
            Student.first_name,
            Student.last_name,
            func.round(func.avg(Grade.score), 2).label('avg_score')
        ).join(Grade).group_by(Student.id, Student.first_name, Student.last_name)\
         .order_by(desc('avg_score')).limit(5).all()
        
        return result
    finally:
        session.close()


def select_2(subject_id):
    session = Session()
    try:
        result = session.query(
            Student.first_name,
            Student.last_name,
            Subject.name.label('subject_name'),
            func.round(func.avg(Grade.score), 2).label('avg_score')
        ).select_from(Student).join(Grade).join(Subject)\
         .filter(Subject.id == subject_id)\
         .group_by(Student.id, Student.first_name, Student.last_name, Subject.name)\
         .order_by(desc('avg_score')).limit(1).all()
        
        return result
    finally:
        session.close()


def select_3(subject_id):
    session = Session()
    try:
        result = session.query(
            Group.name.label('group_name'),
            Subject.name.label('subject_name'),
            func.round(func.avg(Grade.score), 2).label('avg_score')
        ).select_from(Group).join(Student).join(Grade).join(Subject)\
         .filter(Subject.id == subject_id)\
         .group_by(Group.id, Group.name, Subject.name)\
         .order_by(Group.name).all()
        
        return result
    finally:
        session.close()


def select_4():
    session = Session()
    try:
        result = session.query(
            func.round(func.avg(Grade.score), 2).label('avg_score')
        ).scalar()
        
        return result
    finally:
        session.close()


def select_5(teacher_id):
    session = Session()
    try:
        result = session.query(
            Teacher.first_name,
            Teacher.last_name,
            Subject.name.label('subject_name')
        ).join(Subject)\
         .filter(Teacher.id == teacher_id).all()
        
        return result
    finally:
        session.close()


def select_6(group_id):
    session = Session()
    try:
        result = session.query(
            Student.first_name,
            Student.last_name,
            Student.email,
            Group.name.label('group_name')
        ).join(Group)\
         .filter(Group.id == group_id)\
         .order_by(Student.last_name, Student.first_name).all()
        
        return result
    finally:
        session.close()


def select_7(group_id, subject_id):
    session = Session()
    try:
        result = session.query(
            Student.first_name,
            Student.last_name,
            Group.name.label('group_name'),
            Subject.name.label('subject_name'),
            Grade.score,
            Grade.grade_date
        ).select_from(Student).join(Grade).join(Group).join(Subject)\
         .filter(and_(Group.id == group_id, Subject.id == subject_id))\
         .order_by(Student.last_name, Student.first_name, Grade.grade_date).all()
        
        return result
    finally:
        session.close()


def select_8(teacher_id):
    session = Session()
    try:
        result = session.query(
            Teacher.first_name,
            Teacher.last_name,
            func.round(func.avg(Grade.score), 2).label('avg_score')
        ).select_from(Teacher).join(Subject).join(Grade)\
         .filter(Teacher.id == teacher_id)\
         .group_by(Teacher.id, Teacher.first_name, Teacher.last_name).all()
        
        return result
    finally:
        session.close()


def select_9(student_id):
    session = Session()
    try:
        result = session.query(
            Student.first_name,
            Student.last_name,
            Subject.name.label('subject_name')
        ).select_from(Student).join(Grade).join(Subject)\
         .filter(Student.id == student_id)\
         .group_by(Student.id, Student.first_name, Student.last_name, Subject.name)\
         .order_by(Subject.name).all()
        
        return result
    finally:
        session.close()


def select_10(student_id, teacher_id):
    session = Session()
    try:
        result = session.query(
            Student.first_name.label('student_first_name'),
            Student.last_name.label('student_last_name'),
            Teacher.first_name.label('teacher_first_name'),
            Teacher.last_name.label('teacher_last_name'),
            Subject.name.label('subject_name')
        ).select_from(Student).join(Grade).join(Subject).join(Teacher)\
         .filter(and_(Student.id == student_id, Teacher.id == teacher_id))\
         .group_by(Student.id, Student.first_name, Student.last_name,
                  Teacher.id, Teacher.first_name, Teacher.last_name, Subject.name)\
         .order_by(Subject.name).all()
        
        return result
    finally:
        session.close()


if __name__ == "__main__":
    print("1. П'ять студентів із найбільшим середнім балом:")
    for student in select_1():
        print(f"   {student.first_name} {student.last_name}: {student.avg_score}")
    
    print("\n2. Студент із найвищим середнім балом з предмета ID=1:")
    for student in select_2(1):
        print(f"   {student.first_name} {student.last_name} ({student.subject_name}): {student.avg_score}")
    
    print("\n3. Середній бал у групах з предмета ID=1:")
    for group in select_3(1):
        print(f"   {group.group_name} ({group.subject_name}): {group.avg_score}")
    
    print(f"\n4. Середній бал на потоці: {select_4()}")
    
    print("\n5. Курси викладача ID=1:")
    for course in select_5(1):
        print(f"   {course.first_name} {course.last_name} викладає: {course.subject_name}")
    
    print("\n6. Студенти групи ID=1:")
    for student in select_6(1):
        print(f"   {student.first_name} {student.last_name} ({student.email}) - {student.group_name}")
    
    print("\n7. Оцінки студентів групи ID=1 з предмета ID=1 (перші 5):")
    for grade in select_7(1, 1)[:5]:
        print(f"   {grade.first_name} {grade.last_name}: {grade.score} ({grade.grade_date})")
    
    print("\n8. Середній бал викладача ID=1:")
    for teacher in select_8(1):
        print(f"   {teacher.first_name} {teacher.last_name}: {teacher.avg_score}")
    
    print("\n9. Курси студента ID=1:")
    for course in select_9(1):
        print(f"   {course.first_name} {course.last_name} відвідує: {course.subject_name}")
    
    print("\n10. Курси студента ID=1 у викладача ID=1:")
    for course in select_10(1, 1):
        print(f"   {course.student_first_name} {course.student_last_name} вивчає {course.subject_name} у {course.teacher_first_name} {course.teacher_last_name}") 