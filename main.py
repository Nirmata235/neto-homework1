class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def rate_lecture(self, lecturer, course, grade):
        if (isinstance(lecturer, Lecturer)
                and course in lecturer.courses_attached
                and course in self.courses_in_progress):
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def average_grade(self):
        all_grades = [g for grades in self.grades.values() for g in grades]
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за домашние задания: {self.average_grade():.1f}\n'
                f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n'
                f'Завершенные курсы: {", ".join(self.finished_courses)}')

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade() < other.average_grade()

    def __gt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade() > other.average_grade()

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade() == other.average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def average_grade(self):
        all_grades = [g for grades in self.grades.values() for g in grades]
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за лекции: {self.average_grade():.1f}')

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade() < other.average_grade()

    def __gt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade() > other.average_grade()

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade() == other.average_grade()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if (isinstance(student, Student)
                and course in self.courses_attached
                and course in student.courses_in_progress):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}')


# ---------- Функции для подсчёта средних оценок по курсу ----------

def average_hw_by_course(students, course):
    """Средняя оценка за ДЗ по всем студентам в рамках курса."""
    all_grades = []
    for student in students:
        if course in student.grades:
            all_grades += student.grades[course]
    return sum(all_grades) / len(all_grades) if all_grades else 0


def average_lecture_by_course(lecturers, course):
    """Средняя оценка за лекции по всем лекторам в рамках курса."""
    all_grades = []
    for lecturer in lecturers:
        if course in lecturer.grades:
            all_grades += lecturer.grades[course]
    return sum(all_grades) / len(all_grades) if all_grades else 0


# ---------- Полевые испытания ----------

# Создаём по 2 экземпляра каждого класса
student1 = Student('Ruoy', 'Eman', 'M')
student2 = Student('Ольга', 'Алёхина', 'Ж')

lecturer1 = Lecturer('Иван', 'Иванов')
lecturer2 = Lecturer('Пётр', 'Петров')

reviewer1 = Reviewer('Some', 'Buddy')
reviewer2 = Reviewer('Василий', 'Смирнов')

# Настраиваем курсы
student1.courses_in_progress += ['Python', 'Git']
student1.finished_courses += ['Введение в программирование']

student2.courses_in_progress += ['Python', 'Java']
student2.finished_courses += ['Основы ООП']

lecturer1.courses_attached += ['Python', 'Git']
lecturer2.courses_attached += ['Python', 'Java']

reviewer1.courses_attached += ['Python', 'Git']
reviewer2.courses_attached += ['Python', 'Java']

# Reviewer выставляет оценки студентам за ДЗ
reviewer1.rate_hw(student1, 'Python', 10)
reviewer1.rate_hw(student1, 'Python', 9)
reviewer1.rate_hw(student1, 'Git', 8)

reviewer2.rate_hw(student2, 'Python', 7)
reviewer2.rate_hw(student2, 'Python', 9)
reviewer2.rate_hw(student2, 'Java', 10)

# Студенты выставляют оценки лекторам
student1.rate_lecture(lecturer1, 'Python', 10)
student1.rate_lecture(lecturer1, 'Python', 9)
student1.rate_lecture(lecturer1, 'Git', 8)

student2.rate_lecture(lecturer2, 'Python', 7)
student2.rate_lecture(lecturer2, 'Python', 9)
student2.rate_lecture(lecturer2, 'Java', 10)

# Проверка ошибочных вызовов
print(student1.rate_lecture(lecturer2, 'Java', 5))     # Ошибка
print(reviewer1.rate_hw(student2, 'Git', 10))          # Ошибка
print(student1.rate_lecture(reviewer1, 'Python', 5))   # Ошибка

# Печать всех объектов
print('\n--- Reviewer 1 ---')
print(reviewer1)
print('\n--- Reviewer 2 ---')
print(reviewer2)

print('\n--- Lecturer 1 ---')
print(lecturer1)
print('\n--- Lecturer 2 ---')
print(lecturer2)

print('\n--- Student 1 ---')
print(student1)
print('\n--- Student 2 ---')
print(student2)

# Сравнения
print('\n--- Сравнения ---')
print('student1 > student2:', student1 > student2)
print('lecturer1 > lecturer2:', lecturer1 > lecturer2)
print('student1 == student2:', student1 == student2)

# Функции подсчёта средних по курсу
print('\n--- Средние по курсу ---')
print('Средняя за ДЗ по Python:',
      round(average_hw_by_course([student1, student2], 'Python'), 2))
print('Средняя за ДЗ по Git:',
      round(average_hw_by_course([student1, student2], 'Git'), 2))
print('Средняя за лекции по Python:',
      round(average_lecture_by_course([lecturer1, lecturer2], 'Python'), 2))
print('Средняя за лекции по Java:',
      round(average_lecture_by_course([lecturer1, lecturer2], 'Java'), 2))