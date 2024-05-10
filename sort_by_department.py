# Example list of dictionaries
Data = [
    {'name': 'Alice', 'department': 'Human Resources'},
    {'name': 'Bob', 'department': 'Engineering'},
    {'name': 'Charlie', 'department': 'Finance'}
]

# Sorting the list by 'department'
sorted_department = sorted(Data, key=lambda x: x['department'])

print(sorted_department)
