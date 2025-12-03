
try:
    with open("configure.txt", "r") as file:
        content = file.read() 
except FileNotFoundError:
    with open("configure.txt", "w" ) as file:
        file.write("Guest")
    with open("configure.txt", "r") as file:
        content = file.read() 

print("Welcome " + content)


