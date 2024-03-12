import os
import calendar
import pandas as pd

# CSV files
csv_files = ['/Users/glyts/Documents/GitHub/Illuminator/Penelope/CSV/France2022.csv', '/Users/glyts/Documents/GitHub/Illuminator/Penelope/CSV/France2023.csv']

def process_csv(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Split the 'Time (CET/CEST)' column and take the first part (start of the range)
    df['StartDateTime'] = df['Time (CET/CEST)'].apply(lambda x: x.split(' - ')[0])
    
    # Convert 'StartDateTime' to datetime format
    df['StartDateTime'] = pd.to_datetime(df['StartDateTime'], format='%d.%m.%Y %H:%M')
    
    # Extract month and convert month number to month name
    df['Month'] = df['StartDateTime'].dt.month.apply(lambda x: calendar.month_name[x])
    
    # Calculate the average load per month
    avg_load_per_month = df.groupby('Month')['Actual Total Load [MW] - France (FR)'].mean()
    
    # Sort the months by average load, from highest to lowest
    sorted_avg_load = avg_load_per_month.sort_values(ascending=False)
    
    # Format the sorted average loads to have two significant digits after the decimal
    sorted_avg_load = sorted_avg_load.map('{:.2f}'.format)
    
    return sorted_avg_load

# Process each file and print the sorted lists with month names
for csv_file in csv_files:
    sorted_avg_load = process_csv(csv_file)
    print(f"Sorted average load demand for {os.path.basename(csv_file)}:")
    print(sorted_avg_load)
    print("\n")

