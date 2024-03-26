import pandas as pd
import math
import os

#file_path = '/Users/glyts/Documents/GitHub/Illuminator/Penelope/CSV/Household_Consumption.csv'
#data = pd.read_csv(file_path)

# Basic Constants
HOUSES = 10
MONTHS = 6
CONSUMPTION_PER_HOUSE_PER_MONTH_KWH = 300                   # Estimated Consumption of Electricity Sourced from Hydrogen
ENERGY_CONTENT_OF_HYDROGEN_KWH_PER_KG = 33.33
DENSITY_HYDROGEN_KG_M3 = 42                                 # Approximation at 700 bar, considering compressibility 

# Additional Cost Constants
TANK_CAPACITY_IN_KG = 120                                   # Capacity of each tank in kg
STORAGE_TANK_COST_PER_LITER = 0.50                          # $ per liter
HYDROGEN_COST_PER_KG = 10                                   # $ per kg
INSTALLATION_COST_PERCENTAGE = 0.10                         # 10% of tank cost
MAINTENANCE_COST_PERCENTAGE_PER_YEAR = 0.02                 # 2% per year
LIFESPAN_YEARS = 10                                         # Projected lifespan in years

# Safety
SAFETY_MARGIN = 1.15                                        # safety margin

# P2G2P Efficiencies (2024, referenced)
AC_DC_CONVERSION_EFFICIENCY = 0.95
ELECTROLYZER_EFFICIENCY = 0.60                              #Alkaline
STORAGE_EFFICIENCY = 0.90
COMPRESSION_TRANSMISSION_EFFICIENCY = 0.85
FUEL_CELL_EFFICIENCY = 0.60                                 #PEM

# Overall P2G2P cycle efficiency (2024)
TOTAL_EFFICIENCY = (AC_DC_CONVERSION_EFFICIENCY * ELECTROLYZER_EFFICIENCY * STORAGE_EFFICIENCY * COMPRESSION_TRANSMISSION_EFFICIENCY * FUEL_CELL_EFFICIENCY)

# P2G2P Efficiencies (Test Projections)
AC_DC_CONVERSION_EFFICIENCY = 0.95
ELECTROLYZER_EFFICIENCY = 0.70 
STORAGE_EFFICIENCY = 0.95
COMPRESSION_TRANSMISSION_EFFICIENCY = 0.90
FUEL_CELL_EFFICIENCY = 0.80 #PEM

TOTAL_EFFICIENCY1 = (AC_DC_CONVERSION_EFFICIENCY * ELECTROLYZER_EFFICIENCY * STORAGE_EFFICIENCY * COMPRESSION_TRANSMISSION_EFFICIENCY * FUEL_CELL_EFFICIENCY)

# Function 0: Clear Terminal

def clear_terminal():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Linux and macOS
    else:
        os.system('clear')

clear_terminal()
print("Terminal Cleaned!")

# Function 1: Calculation of Hydrogen Capacity (in liters)

def calculate_hydrogen_storage_capacity():                                     # Test 1: Static Data
#def calculate_hydrogen_storage_capacity(data):                                # Test 2: Dynamic Data
    # Total electricity demand
    total_demand_kwh = HOUSES * CONSUMPTION_PER_HOUSE_PER_MONTH_KWH * MONTHS   # Test 1: Static Data
    #total_demand_kwh = data.drop('Month / House', axis=1).to_numpy().sum()    # Test 2: Dynamic Data

    # Energy required in hydrogen form to meet the total demand
    energy_required_in_hydrogen_form_kwh = total_demand_kwh / TOTAL_EFFICIENCY1

    # Mass of hydrogen required to store the calculated energy + safety margin
    hydrogen_mass_required_kg = energy_required_in_hydrogen_form_kwh / ENERGY_CONTENT_OF_HYDROGEN_KWH_PER_KG
    hydrogen_mass_safe_kg = hydrogen_mass_required_kg * SAFETY_MARGIN

    # Converting mass of hydrogen to volume in liters and rounding
    volume_hydrogen_liters = (hydrogen_mass_safe_kg / DENSITY_HYDROGEN_KG_M3) * 1000
    rounded_volume_liters = math.ceil(volume_hydrogen_liters / 10) * 10

    #return energy_required_in_hydrogen_form_kwh, hydrogen_mass_safe_kg, volume_hydrogen_liters, rounded_volume_liters
    return total_demand_kwh, hydrogen_mass_safe_kg, volume_hydrogen_liters, rounded_volume_liters

# Function 2: Determine Number of Tanks

def calculate_number_of_tanks(hydrogen_kg):
    number_of_tanks = math.ceil(hydrogen_kg / TANK_CAPACITY_IN_KG)
    return number_of_tanks

# Function 3: Simple Cost Calculation

def calculate_total_system_cost(volume_liters, hydrogen_mass_required_kg):
    # Calculate storage tank cost
    storage_tank_cost = volume_liters * STORAGE_TANK_COST_PER_LITER
    
    # Installation cost
    installation_cost = storage_tank_cost * INSTALLATION_COST_PERCENTAGE
    
    # Maintenance cost over lifespan
    maintenance_cost = (storage_tank_cost * MAINTENANCE_COST_PERCENTAGE_PER_YEAR) * LIFESPAN_YEARS
    
    # Cost for hydrogen to fill the tank initially
    hydrogen_cost = hydrogen_mass_required_kg * HYDROGEN_COST_PER_KG
    
    # Total system cost
    total_system_cost = storage_tank_cost + installation_cost + maintenance_cost + hydrogen_cost
    
    return total_system_cost

# Calculate required hydrogen storage capacity and hydrogen mass
#energy_required_in_hydrogen_kwh, hydrogen_safe_kg, required_volume_liters, rounded_liters = calculate_hydrogen_storage_capacity()                                #Test 1A: Static Data
hydrogen_needed_kwh, hydrogen_safe_kg, required_volume_liters, rounded_liters = calculate_hydrogen_storage_capacity()                                            #Test 1B: Static Data
#required_volume_liters, required_hydrogen_mass_kg, rounded_liters, required_hydrogen_mass_kg = calculate_hydrogen_storage_capacity(data)                        #Test 2: Dynamic Data

# Calculate the number of hydrogen tanks needed
number_of_tanks_needed = calculate_number_of_tanks(hydrogen_safe_kg)

# Calculate total system cost
total_system_cost = calculate_total_system_cost(required_volume_liters, hydrogen_safe_kg)

# Final Results 

# Print the System Efficiency
print(f"\nSystem Efficiency: {TOTAL_EFFICIENCY1*100:.2f}%\n")

# Print Safety Margin
print(f"Safety Margin: {SAFETY_MARGIN} times the required capacity.\n")

# Print Required Hydrogen Capacity (KG)
# print(f"Required Energy from H2: {energy_required_in_hydrogen_kwh:.2f} KWh\n")
print(f"Required Energy from H2: {hydrogen_needed_kwh:.2f} KWh\n")

# Print Required Hydrogen Capacity (KG)
print(f"Required H2 Capacity: {hydrogen_safe_kg:.2f} KG\n")

print(f"Assuming {CONSUMPTION_PER_HOUSE_PER_MONTH_KWH/30:.2f} KWh has to be spent on a daily basis.\n")

# Print the number of tanks
print(f"Number of ({TANK_CAPACITY_IN_KG} KG) H2 tanks needed: {number_of_tanks_needed}\n")

# Print Total System Cost
print(f"Total system cost: ${total_system_cost:.2f}\n")

# Print Required Hydrogen Capacity
#print(f"Required hydrogen storage capacity with safety margin: {required_volume_liters:.2f} liters\n")

# Print Required Hydrogen Capacity
#print(f"Rounded Volume: {rounded_liters:.2f} liters\n")
