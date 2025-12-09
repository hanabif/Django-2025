try:
    with open("input.txt", "r") as file:
        content = file.read()
        print(content.upper())
except FileNotFoundError:
    print("Error: The file does not exist.")
