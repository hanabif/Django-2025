sales = []

with open("sales.txt", "r") as file:
    for line in file:
        try:
            amount = int(line.strip())
            sales.append(amount)
        except ValueError:
            continue

total_sales = sum(sales)

print("Valid sales:", sales)
print("Total sales:", total_sales)
