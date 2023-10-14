from functools import reduce

orders = [
    {"order_id": 21, "customer_id": 103, "amount": 1150},
    {"order_id": 22, "customer_id": 104, "amount": 1200},
    {"order_id": 23, "customer_id": 105, "amount": 1250},
    {"order_id": 24, "customer_id": 106, "amount": 1300},
    {"order_id": 25, "customer_id": 101, "amount": 1350},
    {"order_id": 26, "customer_id": 102, "amount": 1400},
    {"order_id": 27, "customer_id": 103, "amount": 1450},
    {"order_id": 28, "customer_id": 104, "amount": 1500},
    {"order_id": 29, "customer_id": 105, "amount": 1550},
    {"order_id": 30, "customer_id": 106, "amount": 1600},
    {"order_id": 31, "customer_id": 101, "amount": 1650},
    {"order_id": 32, "customer_id": 102, "amount": 1700},
    {"order_id": 33, "customer_id": 103, "amount": 1750},
    {"order_id": 34, "customer_id": 104, "amount": 1800},
    {"order_id": 35, "customer_id": 105, "amount": 1850},
    {"order_id": 36, "customer_id": 106, "amount": 1900},
    {"order_id": 37, "customer_id": 101, "amount": 1950},
    {"order_id": 38, "customer_id": 102, "amount": 2000},
    {"order_id": 39, "customer_id": 103, "amount": 2050},
    {"order_id": 40, "customer_id": 104, "amount": 2100},
    {"order_id": 41, "customer_id": 105, "amount": 2150},
    {"order_id": 42, "customer_id": 106, "amount": 2200},
    {"order_id": 43, "customer_id": 101, "amount": 2250},
    {"order_id": 44, "customer_id": 102, "amount": 2300},
    {"order_id": 45, "customer_id": 103, "amount": 2350}
]

sort_users_id = list(filter(lambda user: user["customer_id"] == 102, orders))
amounts = list(map(lambda user: user['amount'], sort_users_id))

sum_sort_exps = reduce(lambda x, y: x + y, 
                       amounts, 0)

average_sort_exps = reduce(lambda x, y: x + y,
                           amounts, 0) / len(amounts)

for (index, user) in enumerate(sort_users_id):
    print(f"{index}.:", user)
print(sum_sort_exps)
print(average_sort_exps)