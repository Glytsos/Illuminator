import os
import pandas as pd
from itertools import combinations
from math import factorial

# Define the total shared capacity (X) in units of your choice (e.g., kWh for energy)
total_shared_capacity = 2562.5  # Example value, easily modifiable

file_path = '/Users/glyts/Documents/GitHub/Illuminator/Penelope/CESI.csv'
df = pd.read_csv(file_path)

# Adjusted weights for the CESI components
weights = {"HPI": 0.4, "SCI": 0.2, "EUP": 0.4}

# Calculate max values for normalization
max_HPI = df['HPI'].max()
max_SCI = df['SCI'].max()
max_EUP = df['EUP'].max()

# Calculate CESI for each household
df['CESI'] = (weights['HPI'] * (df['HPI'] / max_HPI) + weights['SCI'] * (df['SCI'] / max_SCI) + weights['EUP'] * (df['EUP'] / max_EUP))

households_data = df.set_index('Household Number')['CESI'].to_dict()

# Total number of households
n = len(households_data)

# Shapley Values calculation
shapley_values = {household: 0 for household in households_data}

def total_cesi(subset):
    return sum(households_data[household] for household in subset)

for household in households_data:
    for S in range(n + 1):
        for subset in combinations(households_data.keys(), S):
            if household not in subset:
                subset_with_household = subset + (household,)
                marginal_contribution = (total_cesi(subset_with_household) - total_cesi(subset))
                shapley_values[household] += (factorial(len(subset)) * factorial(n - len(subset) - 1) / factorial(n)) * marginal_contribution

# Normalizing Shapley Values to reflect their proportion of the total
total_shapley = sum(shapley_values.values())
shapley_values_normalized = {household: value / total_shapley for household, value in shapley_values.items()}

# Calculate each household's fair energy allocation based on the Shapley value percentages
energy_allocations = {household: round(value * total_shared_capacity, 1) for household, value in shapley_values_normalized.items()}

# Printing the Shapley values and energy allocations
print("\nThe Shapley value for each household is:")
for household, percentage in shapley_values_normalized.items():
    print(f"Household {household}: {percentage*100:.1f}%")

print("\nFair energy allocation for each household based on the total shared capacity:")
for household, allocation in energy_allocations.items():
    print(f"Household {household}: {allocation} units")