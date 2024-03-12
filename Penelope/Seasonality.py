import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import calendar
import os

# Function 1: Read CSV files
def read_and_prepare_data(file_path, date_col, load_col, months=None):
    data = pd.read_csv(file_path, usecols=[date_col, load_col])
    data[date_col] = pd.to_datetime(data[date_col].str.split(' - ').str[0], dayfirst=True)
    data.columns = ['Date', 'Load']
    data.set_index('Date', inplace=True)
    
    if months is not None:
        data = data[data.index.month.isin(months)]
        
    return data

# Function 2: Plot 'data' in a single bar Plot
def plot_data(data, months, plot_title, output_file, colors):
    bar_width = 0.35
    indices = np.arange(len(months))
    plt.figure(figsize=(10, 6))

    for i, (label, df) in enumerate(data.items()):
        monthly_data = df.resample('ME').mean()
        monthly_data = monthly_data[monthly_data.index.month.isin(months)]
        monthly_data = monthly_data.sort_index()
        plt.bar(indices + i * bar_width, monthly_data['Load'], label=label, width=bar_width, color=colors[i % len(colors)])

    plt.title(plot_title)
    plt.xlabel('Month')
    plt.ylabel('Average Load per Month in MW')
    plt.xticks(indices + bar_width / 2, [calendar.month_name[month] for month in months], rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

# Function 3: Main Function to output plot
def main(file_paths, months_to_plot, date_column, load_column, plot_title, output_dir, colors):
    data_combined = {}
    for file_path in file_paths:
        country_name = os.path.basename(file_path).split('.')[0]
        data_combined[country_name] = read_and_prepare_data(file_path, date_column, load_column, months=months_to_plot)
    
    output_file = os.path.join(output_dir, 'Spain_Comparison.png')
    plot_data(data_combined, months_to_plot, plot_title, output_file, colors)

# Additional Dependencies
date_column = 'Time (CET/CEST)'
load_column = 'Actual Total Load [MW] - Spain (ES)'
plot_title = 'Load Data Comparison'
colors = ['green', 'blue', '#2ca02c', '#d62728', '#9467bd', '#8c564b'] 
months_to_plot = [1, 2, 3, 10, 11, 12]

output_dir = '/Users/glyts/Documents/GitHub/Illuminator/Penelope/Images'
file_paths = [
    '/Users/glyts/Documents/GitHub/Illuminator/Penelope/CSV/Spain2022.csv',
    '/Users/glyts/Documents/GitHub/Illuminator/Penelope/CSV/Spain2023.csv'
]

main(file_paths, months_to_plot, date_column, load_column, plot_title, output_dir, colors)

print('Process Completed. Plot Generated!')
