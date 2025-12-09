def get_grade(student_grades, student_name):
    try:
        return student_grades[student_name]
    except KeyError:
        return "Student not found in the system"


# Example
grades = {
    "Alice": 88,
    "Bob": 92,
    "Charlie": 79
}

print(get_grade(grades, "Diana"))
