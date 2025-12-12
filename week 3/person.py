class Person:
    def __init__(self,name,age):
       self.name = name
       self.age = age
    def Pr(self):
        print(f"{self.name}, {self.age}")
person = Person("Amy", 22)
print(person.Pr())
