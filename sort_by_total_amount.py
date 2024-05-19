# Example list of dictionaries
data = [
    {'name': 'Alice', 'total_spent': 250.50},
    {'name': 'Bob', 'total_spent': 150.75},
    {'name': 'Charlie', 'total_spent': 300.20}
]

# Sorting the list by 'total_spent'
sorted_amount = sorted(data, key=lambda x: x['total_spent'])

print(sorted_amount)
