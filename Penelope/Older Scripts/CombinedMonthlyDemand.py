# Data extracted from the document for the months October to March for both 2022 and 2023 across four countries.
# Each entry is [month, year2022, year2023]
# This has been used in the report to showcase some of the extrapolated data.

data = {
    "Spain": {
        "October": [24547.17, 24817.37],
        "November": [25560.27, 26075.18],
        "December": [25944.21, 26812.17],
        "January": [28935.10, 28082.67],
        "February": [28471.93, 28785.25],
        "March": [27340.52, 26097.13],
    },
    "Greece": {
        "October": [4602.49, 4899.66],
        "November": [4832.65, 4943.38],
        "December": [5278.48, 5446.78],
        "January": [6375.68, 5413.28],
        "February": [6095.33, 5739.09],
        "March": [6180.73, 5098.04],
    },
    "Netherlands": {
        "October": [11084.88, 12923.63],
        "November": [12237.46, 13711.00],
        "December": [13008.14, 14219.95],
        "January": [13333.70, 12804.86],
        "February": [12728.95, 12096.80],
        "March": [11270.55, 11455.17],
    },
    "France": {
        "October": [42627.18, 43249.11],
        "November": [50520.18, 52953.41],
        "December": [60638.79, 57774.56],
        "January": [69361.65, 62019.97],
        "February": [62665.12, 60526.76],
        "March": [56141.19, 52954.86],
    }
}

# Calculate the average load demand for each month by averaging the values from 2022 and 2023, then rank them.
average_load_demand = {month: 0 for month in data["Spain"]}  # Initialize with months

for country in data:
    for month in data[country]:
        # Average for each month for a country
        month_avg = sum(data[country][month]) / len(data[country][month])
        # Add to the total average, will divide by the number of countries at the end
        average_load_demand[month] += month_avg

# Average across all countries
average_load_demand = {month: demand / len(data) for month, demand in average_load_demand.items()}

# Sort the months by average load demand in descending order
sorted_months = sorted(average_load_demand.items(), key=lambda x: x[1], reverse=True)

print(sorted_months)
