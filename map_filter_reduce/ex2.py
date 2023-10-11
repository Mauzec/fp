from functools import reduce

users = [
    {"name": "Alice", "expenses": [100, 50, 75, 200]},
    {"name": "Bob", "expenses": [50, 75, 80, 100]},
    {"name": "Charlie", "expenses": [200, 300, 50, 150]},
    {"name": "David", "expenses": [100, 200, 300, 400]},
]

def filterUsers(users, criteria:dict):
    return filter(lambda user: user["name"] in criteria["name"] and 
                  all(expense in user["expenses"] for expense in criteria["expenses"]), 
                  users)


def totalExpenses(user):
    return sum(user["expenses"])

def totalAllExpenses(users):
    return reduce(lambda x, y: x + y, map(totalExpenses, users), 0)

print("Criteria[Alice, Bob, 100, 50]:")
filters = list(filterUsers(users, {"name": ["Alice", "Bob"], "expenses": [100, 50]}))
for user in filters:
    print(f"--- {user}")
    print(f"--- total: {totalExpenses(user)}")
    print()

print(f"All: {totalAllExpenses(filters)}")

