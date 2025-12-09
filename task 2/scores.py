scores = {"John": 85, "Sara": 92, "Fraol": 78}

student_name = input("Enter the student's name: ")

try:
    print(f"{student_name}'s score is {scores[student_name]}")
except KeyError:
    print("Student not found!")
