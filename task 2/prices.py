def get(prices):
    return [price for price in prices if price > 100]

prices = [120, 45, 300, 85, 150]
print(get(prices))
