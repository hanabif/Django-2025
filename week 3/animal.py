class Animal:
    def make_sound(self):
        print("Some animal sound")

class Cat(Animal):
    def make_sound(self):
        print("Meow")

a = Animal()
c = Cat()

a.make_sound()
c.make_sound()
