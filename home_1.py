class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def get_average_grade(self):
        all_grades = []
        for grades in self.grades.values():
            all_grades.extend(grades)

        if not all_grades:
            return 0
        return sum(all_grades) / len(all_grades)

    def get_courses_in_progress(self):
        return ', '.join(map(str, self.courses_in_progress))

    def get_finished_courses(self):
        return ', '.join(map(str, self.finished_courses))

    def __str__(self):
        result = (f'Имя: {self.name} \n'
                f'Фамилия: {self.surname} \n'
                f'Средняя оценка за домашние задания: {self.get_average_grade()} \n'
                f'Курсы в процессе изучения: {self.get_courses_in_progress()}, \n'
                f'Завершенные курсы: {self.get_finished_courses()}')
        return result


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        result = (f'Имя: {self.name} \n'
                  f'Фамилия: {self.surname}')
        return result

class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        result = (f'Имя: {self.name} \n'
                f'Фамилия: {self.surname} \n'
                f'Средняя оценка за лекции: {self.get_average_grade()}')
        return result

    def get_average_grade(self):
        all_grades = []
        for grades in self.grades.values():
            all_grades.extend(grades)

        if not all_grades:
            return 0
        return sum(all_grades) / len(all_grades)

class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


def average_grade_students(students_list, course_name):
    all_grades = []
    for student in students_list:
        if course_name in student.grades:
            all_grades.extend(student.grades[course_name])
    return sum(all_grades) / len(all_grades) if all_grades else 0


def average_grade_lecturers(lecturers_list, course_name):
    all_grades = []
    for lecturer in lecturers_list:
        if course_name in lecturer.grades:
            all_grades.extend(lecturer.grades[course_name])
    return sum(all_grades) / len(all_grades) if all_grades else 0


student1 = Student('Иван', 'Иванов', 'М')
student1.courses_in_progress += ['Python', 'Git']
student1.finished_courses += ['Введение в программирование']

student2 = Student('Ольга', 'Алёхина', 'Ж')
student2.courses_in_progress += ['Python']
student2.finished_courses += ['Введение в программирование', 'Git']

lecturer1 = Lecturer('Семен', 'Васильев')
lecturer1.courses_attached += ['Python', 'Git']

lecturer2 = Lecturer('Петр', 'Петров')
lecturer2.courses_attached += ['Python', 'JavaScript']

reviewer1 = Reviewer('Алексей', 'Алексеев')
reviewer1.courses_attached += ['Python', 'Git']

reviewer2 = Reviewer('Мария', 'Сидорова')
reviewer2.courses_attached += ['Python', 'JavaScript']

reviewer1.rate_hw(student1, 'Python', 9)
reviewer1.rate_hw(student1, 'Python', 10)
reviewer1.rate_hw(student1, 'Git', 8)

reviewer2.rate_hw(student2, 'Python', 8)
reviewer2.rate_hw(student2, 'Python', 9)
reviewer2.rate_hw(student2, 'JavaScript', 10)

student1.rate_lecture(lecturer1, 'Python', 10)
student1.rate_lecture(lecturer1, 'Git', 9)
student1.rate_lecture(lecturer2, 'Python', 8)

student2.rate_lecture(lecturer1, 'Python', 9)
student2.rate_lecture(lecturer2, 'Python', 10)
student2.rate_lecture(lecturer2, 'JavaScript', 9)

