class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def annual_salary(self):
        return self.salary * 12

e = Employee("John", 5000)
print(e.annual_salary())
