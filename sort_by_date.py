from datetime import datetime

# List of date strings
data = ['2023-04-15', '2021-05-10', '2022-12-01']

# Sorting the dates
sorted_dates = sorted(data, key=lambda date: datetime.strptime(date, '%Y-%m-%d'))

print(sorted_dates)
