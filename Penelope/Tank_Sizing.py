import pandas as pd
import math

file_path = '/Users/glyts/Documents/GitHub/Illuminator/Penelope/CSV/Household_Consumption.csv'
data = pd.read_csv(file_path)

# Basic Constants
HOUSES = 10
MONTHS = 6
CONSUMPTION_PER_HOUSE_PER_MONTH_KWH = 500
ENERGY_CONTENT_OF_HYDROGEN_KWH_PER_KG = 33.33
DENSITY_HYDROGEN_KG_M3 = 42 # Approximation at 700 bar

# Additional Cost Constants
STORAGE_TANK_COST_PER_LITER = 0.50 # $ per liter
HYDROGEN_COST_PER_KG = 10 # $ per kg
INSTALLATION_COST_PERCENTAGE = 0.10 # 10% of tank cost
MAINTENANCE_COST_PERCENTAGE_PER_YEAR = 0.02 # 2% per year
LIFESPAN_YEARS = 10 # Projected lifespan in years

# Safety
SAFETY_MARGIN = 1.10 # 10% safety margin

# P2G2P Efficiencies (2024, referenced)
AC_DC_CONVERSION_EFFICIENCY = 0.95
ELECTROLYZER_EFFICIENCY = 0.60  #Alkaline
STORAGE_EFFICIENCY = 0.90
COMPRESSION_TRANSMISSION_EFFICIENCY = 0.85
FUEL_CELL_EFFICIENCY = 0.60 #PEM

# Overall P2G2P cycle efficiency (2024)
TOTAL_EFFICIENCY = (AC_DC_CONVERSION_EFFICIENCY * ELECTROLYZER_EFFICIENCY * STORAGE_EFFICIENCY * COMPRESSION_TRANSMISSION_EFFICIENCY * FUEL_CELL_EFFICIENCY)

# P2G2P Efficiencies (Test Projections)
AC_DC_CONVERSION_EFFICIENCY = 0.95
ELECTROLYZER_EFFICIENCY = 0.70  #Alkaline
STORAGE_EFFICIENCY = 0.95
COMPRESSION_TRANSMISSION_EFFICIENCY = 0.90
FUEL_CELL_EFFICIENCY = 0.80 #PEM

TOTAL_EFFICIENCY1 = (AC_DC_CONVERSION_EFFICIENCY * ELECTROLYZER_EFFICIENCY * STORAGE_EFFICIENCY * COMPRESSION_TRANSMISSION_EFFICIENCY * FUEL_CELL_EFFICIENCY)

# Function 1: Calculation of Hydrogen Capacity (in liters)
def calculate_hydrogen_storage_capacity(data):
    # Total electricity demand
    total_demand_kwh = data.drop('Month / House', axis=1).to_numpy().sum()

    # Energy required in hydrogen form to meet the total demand
    energy_required_in_hydrogen_form_kwh = total_demand_kwh / TOTAL_EFFICIENCY1

    # Mass of hydrogen required to store the calculated energy
    hydrogen_mass_required_kg = energy_required_in_hydrogen_form_kwh / ENERGY_CONTENT_OF_HYDROGEN_KWH_PER_KG

    # Converting mass of hydrogen to volume in liters
    volume_hydrogen_liters = (hydrogen_mass_required_kg / DENSITY_HYDROGEN_KG_M3) * 1000

    # Adding a 10% safety margin to the volume
    volume_with_safety_margin_liters = volume_hydrogen_liters * SAFETY_MARGIN

    # Rounded Volume of Hydrogen Tank   
    rounded_volume_liters = math.ceil(volume_with_safety_margin_liters / 1000) * 1000

    return volume_with_safety_margin_liters, hydrogen_mass_required_kg, rounded_volume_liters, hydrogen_mass_required_kg


# Function 2: Simple Cost Calculation
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
required_volume_liters, required_hydrogen_mass_kg, rounded_liters, required_hydrogen_mass_kg = calculate_hydrogen_storage_capacity(data)

# Calculate total system cost
total_system_cost = calculate_total_system_cost(required_volume_liters, required_hydrogen_mass_kg)

# Print the System Efficiency
print(f"\nTotal P2G2P System Efficiency: {TOTAL_EFFICIENCY1*100:.2f}%\n")

# Print Required Hydrogen Capacity (KG)
print(f"Required KG of H2 (10% safety margin): {required_hydrogen_mass_kg:.2f} KG\n")

# Print Required Hydrogen Capacity
print(f"Required hydrogen storage capacity with 10% safety margin: {required_volume_liters:.2f} liters\n")

# Print Required Hydrogen Capacity
print(f"Rounded Volume: {rounded_liters:.2f} liters\n")

# Print System Cost
print(f"Total system cost for the hydrogen storage system: ${total_system_cost:.2f}\n")


#def calculate_hydrogen_storage_capacity():
    # Total electricity demand for 6 months
    #total_demand_kwh = HOUSES * CONSUMPTION_PER_HOUSE_PER_MONTH_KWH * MONTHS

    # Energy required in hydrogen form to meet the total demand
    #energy_required_in_hydrogen_form_kwh = total_demand_kwh / TOTAL_EFFICIENCY

    # Mass of hydrogen required to store the calculated energy
    #hydrogen_mass_required_kg = energy_required_in_hydrogen_form_kwh / ENERGY_CONTENT_OF_HYDROGEN_KWH_PER_KG

    # Converting mass of hydrogen to volume in liters
    #volume_hydrogen_liters = (hydrogen_mass_required_kg / DENSITY_HYDROGEN_KG_M3) * 1000

    # Adding a 10% safety margin to the volume
    #volume_with_safety_margin_liters = volume_hydrogen_liters * SAFETY_MARGIN

    #return volume_with_safety_margin_liters

#print(f"Total Efficiency: {TOTAL_EFFICIENCY:.2f} %")

# Calculate and print the required hydrogen storage capacity
#required_hydrogen_storage_capacity_liters = calculate_hydrogen_storage_capacity()
#print(f"Required hydrogen storage capacity with 10% safety margin: {required_hydrogen_storage_capacity_liters:.2f} liters")


#def calculate_total_system_cost(volume_liters, hydrogen_mass_required_kg):
    # Calculate storage tank cost
    #storage_tank_cost = volume_liters * STORAGE_TANK_COST_PER_LITER
    
    # Installation cost
    #installation_cost = storage_tank_cost * INSTALLATION_COST_PERCENTAGE
    
    # Maintenance cost over lifespan
    #maintenance_cost = (storage_tank_cost * MAINTENANCE_COST_PERCENTAGE_PER_YEAR) * LIFESPAN_YEARS
    
    # Cost for hydrogen to fill the tank initially
    #hydrogen_cost = hydrogen_mass_required_kg * HYDROGEN_COST_PER_KG
    
    # Total system cost
    #total_system_cost = storage_tank_cost + installation_cost + maintenance_cost + hydrogen_cost
    
    #return total_system_cost

# Calculate required hydrogen storage capacity
#required_volume_liters = calculate_hydrogen_storage_capacity()
#required_hydrogen_mass_kg = required_volume_liters / 1000 * DENSITY_HYDROGEN_KG_M3 / SAFETY_MARGIN

# Calculate and print the total system cost
#total_system_cost = calculate_total_system_cost(required_volume_liters, required_hydrogen_mass_kg)
#print(f"Total system cost for the hydrogen storage system: ${total_system_cost:.2f}")
