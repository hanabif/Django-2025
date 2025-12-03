from datetime import datetime

age = int(input("Enter your age: "))
current_year = datetime.now().year
birth_year = current_year - age

print("You were born in", birth_year)
