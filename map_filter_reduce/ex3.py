from functools import reduce

orders = [
    {"order_id": 1, "customer_id": 101, "amount": 150.0},
    {"order_id": 2, "customer_id": 102, "amount": 200.0},
    {"order_id": 3, "customer_id": 101, "amount": 75.0},
    {"order_id": 4, "customer_id": 103, "amount": 100.0},
    {"order_id": 5, "customer_id": 101, "amount": 50.0},
]

customerId = 101
# filter
filterOrders = list(filter(lambda order: order["customer_id"] == customerId, orders))
# sum amount
amount = reduce(lambda x, y: x + y["amount"], filterOrders, 0)
# av amount
numOfOrders = len(filterOrders)
average = amount / numOfOrders if numOfOrders > 0 else 0.0

print(list(filterOrders), amount, average, sep="\n\n")