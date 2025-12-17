from abc import ABC, abstractmethod

class Employee(ABC):
    @abstractmethod
    def calculate_salary(self):
        pass
class FullTimeEmployee(Employee):
    def calculate_salary(self):
        return self.annual_salary / 12  
    
emp = FullTimeEmployee()
emp.annual_salary = 60000
print(emp.calculate_salary())
