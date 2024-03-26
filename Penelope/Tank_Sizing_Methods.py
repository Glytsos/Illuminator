import pandas as pd
import math
import os

HOUSES = 10
MONTHS = 6
CONSUMPTION_PER_HOUSE_PER_MONTH_KWH = 250                   # Estimated Consumption of Electricity Sourced from Hydrogen
ENERGY_CONTENT_OF_HYDROGEN_KWH_PER_KG = 33.33
DENSITY_HYDROGEN_KG_M3 = 42                                 # Approximation at 700 bar, considering compressibility 

TANK_CAPACITY_IN_KG = 120                                   # Capacity of each tank in kg
STORAGE_TANK_COST_PER_LITER = 0.50                          # $ per liter
HYDROGEN_COST_PER_KG = 10                                   # $ per kg
INSTALLATION_COST_PERCENTAGE = 0.10                         # 10% of tank cost
MAINTENANCE_COST_PERCENTAGE_PER_YEAR = 0.02                 # 2% per year
LIFESPAN_YEARS = 10                                         # Projected lifespan in years

SAFETY_MARGIN = 1.10                                        # safety margin

# P2G2P Efficiencies (2024, referenced)
AC_DC_CONVERSION_EFFICIENCY = 0.95
ELECTROLYZER_EFFICIENCY = 0.60                              # Alkaline Electrolyser
STORAGE_EFFICIENCY = 0.90
COMPRESSION_TRANSMISSION_EFFICIENCY = 0.85
FUEL_CELL_EFFICIENCY = 0.60                                 # PEM Fuel Cell
TOTAL_EFFICIENCY = (AC_DC_CONVERSION_EFFICIENCY * ELECTROLYZER_EFFICIENCY * STORAGE_EFFICIENCY * COMPRESSION_TRANSMISSION_EFFICIENCY * FUEL_CELL_EFFICIENCY)

# P2G2P Efficiencies (Test Projections)
AC_DC_CONVERSION_EFFICIENCY = 0.95
ELECTROLYZER_EFFICIENCY = 0.70 
STORAGE_EFFICIENCY = 0.95
COMPRESSION_TRANSMISSION_EFFICIENCY = 0.90
FUEL_CELL_EFFICIENCY = 0.80
TOTAL_EFFICIENCY1 = (AC_DC_CONVERSION_EFFICIENCY * ELECTROLYZER_EFFICIENCY * STORAGE_EFFICIENCY * COMPRESSION_TRANSMISSION_EFFICIENCY * FUEL_CELL_EFFICIENCY)

# Function 1: Clear Terminal

def clear_terminal():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Linux and macOS
    else:
        os.system('clear')

clear_terminal()
print("Terminal Cleared. ")

# Function 2: Hydrogen Capacity Calculations

def calculate_hydrogen_storage_capacity():                                     
    
    total_demand_kwh = HOUSES * CONSUMPTION_PER_HOUSE_PER_MONTH_KWH * MONTHS                                        # Total electricity demand to be covered from hydrogen

    energy_required_in_hydrogen_form_kwh = total_demand_kwh / TOTAL_EFFICIENCY1                                     # Energy in kWh required in hydrogen form to meet the total demand number

    hydrogen_mass_required_kg = energy_required_in_hydrogen_form_kwh / ENERGY_CONTENT_OF_HYDROGEN_KWH_PER_KG        # Mass of hydrogen required to store the calculated energy
    hydrogen_mass_safe_kg = hydrogen_mass_required_kg * SAFETY_MARGIN                                               # Safety Margin

    volume_hydrogen_liters = (hydrogen_mass_safe_kg / DENSITY_HYDROGEN_KG_M3) * 1000                                # Converting mass of hydrogen to volume in liters 
    rounded_volume_liters = math.ceil(volume_hydrogen_liters / 10) * 10                                             # Rounded Final Value

    return energy_required_in_hydrogen_form_kwh, hydrogen_mass_safe_kg, volume_hydrogen_liters, rounded_volume_liters

tot_demand_hydro_kwh, hydrogen_safe_kg, required_volume_liters, rounded_liters = calculate_hydrogen_storage_capacity()                                            #Test 1B: Static Data

# Function 3: Determine Number of Tanks

def calculate_number_of_tanks(hydrogen_kg):
    number_of_tanks = math.ceil(hydrogen_kg / TANK_CAPACITY_IN_KG)
    return number_of_tanks

number_of_tanks_needed = calculate_number_of_tanks(hydrogen_safe_kg)

# Function 4: Simple Cost Calculation

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

total_system_cost = calculate_total_system_cost(required_volume_liters, hydrogen_safe_kg)

# Final Results 

# Print the System Efficiency
print(f"\nSystem Efficiency: {TOTAL_EFFICIENCY1*100:.2f}%\n")

# Print Safety Margin
print(f"Safety Margin: {SAFETY_MARGIN} times the required capacity.\n")

# Print Required Hydrogen Capacity
print(f"This would require a total of {tot_demand_hydro_kwh:.2f} KWh or {hydrogen_safe_kg:.2f} KG of Hydrogen.\n")

# Print the number of tanks
print(f"Number of ({TANK_CAPACITY_IN_KG} KG) H2 tanks needed: {number_of_tanks_needed}\n")

# Print Total System Cost
print(f"Total system cost: ${total_system_cost:.2f}\n")

# Print Required Hydrogen Capacity
#print(f"Required hydrogen storage capacity with safety margin: {required_volume_liters:.2f} liters\n")

# Print Required Hydrogen Capacity
#print(f"Rounded Volume: {rounded_liters:.2f} liters\n")

