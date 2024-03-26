import pandas as pd

def rank_days_by_energy_consumption(file_path):
    # Load the CSV file
    data = pd.read_csv(file_path)

    # Extract the date from the "Time (CET/CEST)" column (taking the first date in the range)
    data['Date'] = pd.to_datetime(data['Time (CET/CEST)'].str.split(' - ').str[0], dayfirst=True)

    # Determine the day of the week from the 'Date' column (Monday=0, Sunday=6)
    data['DayOfWeek'] = data['Date'].dt.dayofweek

    # Map the day of the week to actual day names
    days_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    data['DayName'] = data['DayOfWeek'].map(days_map)

    # Aggregate the data by day of the week and calculate the average energy consumption
    average_consumption_by_day = data.groupby('DayName')['Actual Total Load [MW] - Netherlands (NL)'].mean()

    # Sort the days from highest to lowest average energy consumption
    ranked_days = average_consumption_by_day.sort_values(ascending=False)

    # Print the ranked days and their average energy consumption
    for day, avg_consumption in ranked_days.items():
        print(f"{day}: {avg_consumption:.2f} MW")

# Path to the CSV file
file_path = '/Users/glyts/Documents/GitHub/Illuminator/Penelope/CSV/Netherlands2022.csv'

# Run the function
rank_days_by_energy_consumption(file_path)
