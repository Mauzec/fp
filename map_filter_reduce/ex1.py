from functools import reduce

students = [
    {'name': 'Elena', 'age': 19, 'grades': [4, 4, 3, 5]},
    {'name': 'Ivan', 'age': 20, 'grades': [3, 2, 4, 3]},
    {'name': 'Olga', 'age': 22, 'grades': [5, 4, 5, 3]},
    {'name': 'Dmitri', 'age': 21, 'grades': [3, 3, 4, 2]},
    {'name': 'Svetlana', 'age': 20, 'grades': [4, 5, 4, 4]},
    {'name': 'Vladimir', 'age': 23, 'grades': [5, 3, 4, 5]},
    {'name': 'Natalia', 'age': 20, 'grades': [4, 4, 4, 4]},
    {'name': 'Mikhail', 'age': 22, 'grades': [4, 5, 5, 4]},
    {'name': 'Yulia', 'age': 21, 'grades': [3, 2, 3, 3]},
    {'name': 'Pavel', 'age': 23, 'grades': [4, 4, 4, 4]},
    {'name': 'Ekaterina', 'age': 20, 'grades': [5, 4, 5, 3]},
    {'name': 'Sergei', 'age': 22, 'grades': [2, 3, 3, 4]},
    {'name': 'Marina', 'age': 21, 'grades': [4, 5, 5, 4]},
    {'name': 'Andrei', 'age': 20, 'grades': [3, 4, 3, 2]},
    {'name': 'Tatiana', 'age': 23, 'grades': [4, 5, 4, 4]},
    {'name': 'Viktor', 'age': 20, 'grades': [3, 2, 4, 3]},
    {'name': 'Nina', 'age': 22, 'grades': [5, 4, 5, 3]},
    {'name': 'Alexey', 'age': 21, 'grades': [2, 3, 3, 2]},
    {'name': 'Irina', 'age': 20, 'grades': [4, 4, 3, 5]},
    {'name': 'Oleg', 'age': 23, 'grades': [5, 5, 4, 5]},
    {'name': 'Yuri', 'age': 20, 'grades': [4, 3, 4, 4]},
    {'name': 'Eva', 'age': 22, 'grades': [3, 4, 4, 3]},
    {'name': 'Maxim', 'age': 21, 'grades': [5, 5, 5, 4]},
    {'name': 'Larisa', 'age': 20, 'grades': [3, 3, 4, 2]},
    {'name': 'Gleb', 'age': 23, 'grades': [4, 4, 3, 4]}
]

students_20_older = list(filter(lambda student: student['age'] >= 20, students))
average_grades = list(map(lambda student: reduce(lambda x,y: x + y, student['grades'], 0) / 
                          len(student['grades']), students))
global_average_grade = reduce(lambda x,y: x + y, average_grades, 0) / len(average_grades)

best_students_by_average = list(filter(lambda student: 
    reduce(lambda x,y: x + y, student['grades'], 0) == 
    max(list(map(lambda st: reduce(lambda x,y: x + y, st['grades'], 0), students))), students
))

print("Students that are 20 years old or older: ")
for (index, student) in enumerate(students_20_older):
    print(f"{index}:", student)
print("Average grade for everyone: ")
for (index, grade) in enumerate(average_grades):
    print(f"{index}:", grade)
print("Average grade global: ", global_average_grade)
print("Best students by average grades")
for student in best_students_by_average:
    print(student)