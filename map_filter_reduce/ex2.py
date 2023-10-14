from functools import reduce

users = [
    {"name": "Eve", "expenses": [50, 60, 70, 80]},
    {"name": "Frank", "expenses": [75, 85, 95, 105]},
    {"name": "Grace", "expenses": [90, 100, 110, 120]},
    {"name": "Hank", "expenses": [130, 140, 150, 160]},
    {"name": "Ivy", "expenses": [170, 180, 190, 200]},
    {"name": "Jack", "expenses": [60, 70, 80, 90]},
    {"name": "Kelly", "expenses": [80, 90, 100, 110]},
    {"name": "Liam", "expenses": [110, 120, 130, 140]},
    {"name": "Mia", "expenses": [130, 140, 150, 160]},
    {"name": "Nora", "expenses": [160, 170, 180, 190]},
    {"name": "Oliver", "expenses": [200, 210, 220, 230]},
    {"name": "Penny", "expenses": [240, 250, 260, 270]},
    {"name": "Quinn", "expenses": [70, 80, 90, 100]},
    {"name": "Riley", "expenses": [90, 100, 110, 120]},
    {"name": "Sam", "expenses": [120, 130, 140, 150]},
    {"name": "Tom", "expenses": [150, 160, 170, 180]},
    {"name": "Uma", "expenses": [190, 200, 210, 220]},
    {"name": "Victor", "expenses": [210, 220, 230, 240]},
    {"name": "Wendy", "expenses": [70, 80, 90, 100]},
    {"name": "Xander", "expenses": [90, 100, 110, 120]},
    {"name": "Yara", "expenses": [110, 120, 130, 140]},
    {"name": "Zane", "expenses": [130, 140, 150, 160]},
    {"name": "Luna", "expenses": [160, 170, 180, 190]},
    {"name": "Max", "expenses": [200, 210, 220, 230]},
    {"name": "Ava", "expenses": [240, 250, 260, 270]},
]

sort_users = list(filter(lambda user: reduce(lambda x, y: x + y, user['expenses'], 0) >= 900, users))
total_expenses_sort_users = list(map(lambda user: reduce(lambda x, y: x + y, user['expenses'], 0), sort_users))

total_expenses_all_users = list(map(lambda user: reduce(lambda x, y: x + y, user['expenses'], 0), users))

print("Users with expenses more 900:")
for (index, user) in enumerate(sort_users):
    print(f"{index}.:", user)
print("[For sorted] Total expenses:")
for (index, exp) in enumerate(total_expenses_sort_users):
    print(f"{index}.:", exp)
print("[For all] Total expenses:")
for (index, exp) in enumerate(total_expenses_all_users):
    print(f"{index}.:", exp)

