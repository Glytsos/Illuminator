# Version 2.0: Added Monthly weights

import pandas as pd
from itertools import combinations
from math import factorial

# Define total shared capacity in Kilowatt-hours (kWh)
total_shared_capacity = 18000  

# Monthly weights based on energy demand assessment script
monthly_weights = {
    'January': 0.22,
    'February': 0.20,
    'December': 0.18,
    'March': 0.16,
    'November': 0.14,
    'October': 0.10
}

# Adjusted weights for the CESI components
weights = {"HPI": 0.4, "SCI": 0.2, "EUP": 0.4}

# Read the CSV file
df = pd.read_csv('/Users/glyts/Documents/GitHub/Illuminator/Penelope/CSV/CESI.csv')

# Calculate max values for normalization
max_HPI = df['HPI'].max()
max_SCI = df['SCI'].max()
max_EUP = df['EUP'].max()

# Calculate CESI for each household
df['CESI'] = (weights['HPI'] * (df['HPI'] / max_HPI) + 
              weights['SCI'] * (df['SCI'] / max_SCI) + 
              weights['EUP'] * (df['EUP'] / max_EUP))

households_data = df.set_index('Household Number')['CESI'].to_dict()

# Shapley Values calculation
shapley_values = {household: 0 for household in households_data}

def total_cesi(subset):
    return sum(households_data[household] for household in subset)

n = len(households_data)  # Total number of households

for household in households_data:
    for S in range(n + 1):
        for subset in combinations(households_data.keys(), S):
            if household not in subset:
                subset_with_household = subset + (household,)
                marginal_contribution = total_cesi(subset_with_household) - total_cesi(subset)
                shapley_values[household] += (factorial(len(subset)) * factorial(n - len(subset) - 1) / factorial(n)) * marginal_contribution

# Normalizing Shapley Values
total_shapley = sum(shapley_values.values())
shapley_values_normalized = {household: value / total_shapley for household, value in shapley_values.items()}

# Monthly allocations based on Shapley values and unique monthly weights
monthly_allocations = {month: {} for month in monthly_weights}
for month, weight in monthly_weights.items():
    for household, shapley_value in shapley_values_normalized.items():
        monthly_allocation = round(shapley_value * weight * total_shared_capacity, 1)
        monthly_allocations[month][household] = monthly_allocation

# Print the results
print("\nMonthly fair energy allocation (in kWh) for each household:")
for month, allocations in monthly_allocations.items():
    print(f"\n{month}:")
    for household, allocation in allocations.items():
        print(f"Household {household}: {allocation} kWh")
