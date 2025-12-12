class Vehicle:
    def __init__(self, brand, year):
        self.brand = brand
        self.year = year

    def info(self):
        print(f"Brand: {self.brand}, Year: {self.year}")

class Car(Vehicle):
    def __init__(self, brand, year, model):
        super().__init__(brand, year)
        self.model = model

    def info(self):  # overridden
        print(f"{self.brand} {self.model} ({self.year})")

v = Vehicle("Ford", 2010)
c = Car("Toyota", 2020, "Corolla")

v.info()
c.info()
