with open("log.txt", "a") as file:
    file.write("User logged in\n")


with open("log.txt", "r") as file:
    log_history = file.read()
    print(log_history)
