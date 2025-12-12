class Student:
    def __init__(self):
        self.__grade = None

    def set_grade(self, grade):
        self.__grade = grade

    def get_grade(self):
        return self.__grade

s = Student()
s.set_grade("A")
print(s.get_grade())
