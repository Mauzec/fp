from functools import reduce

def filterStudents(students, ageRange=None, subjects=None):
    if ageRange != None and subjects != None:
        return filter(lambda student: (student["age"] >= ageRange[0] and student["age"] <= ageRange[1] and
                      all(subject in student["subjects"] for subject in subjects)), students)
    elif ageRange != None:
        return filter(lambda student: student["age"] >= ageRange[0] and student["age"] <= ageRange[1], students)
    elif subjects != None:
        return filter(lambda student: all(subject in student["subjects"] for subject in subjects), students)
    return []

def averageGrade(student):
    grades = student["grades"]
    return sum(grades) / len(grades)

def averageAllGrades(students):
    avGrades = list(map(averageGrade, students))
    return reduce(lambda x, y: x + y, avGrades) / len(avGrades)

def bestStudents(students):
    highAv = max(map(averageGrade, students))
    return [student for student in students if averageGrade(student) == highAv]
    


students = [
    {"name": "Alice", "age": 20, "grades": [85, 90, 88, 92], "subjects": ["astro", "math", "biology", "func"]}, 
    {"name": "Bob", "age": 22, "grades": [78, 89, 76, 85], "subjects": ["math", "biology", "func"]}, 
    {"name": "Charlie", "age": 21, "grades": [92, 95, 88, 94], "subjects": ["biology", "func"]}
]

print("Filter:")
print("--- subjects[math]: ")
for student in filterStudents(students, None, ["math"]):
    print(f"------ {student}")
print("--- age[20...21]: ")
for student in filterStudents(students, [20, 21], None):
    print(f"------ {student}")
print("--- age[20...21], subjects[math]: ")
for student in filterStudents(students, [20, 21], ["math"]):
    print(f"------ {student}")

print("Average grade:")
print("--- first student: ")
print(f"------ {averageGrade(students[0])}")
print("--- all average: ")
print(f"----- {averageAllGrades(students)}")

print("--- Best students: ")
for student in bestStudents(students):
    print(f"------ {student}")