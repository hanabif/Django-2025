class Car:
    def __init__(self, make):
        self.make = make

    def get_make(self):
        return self.make

c = Car("Toyota")
print(c.get_make())
