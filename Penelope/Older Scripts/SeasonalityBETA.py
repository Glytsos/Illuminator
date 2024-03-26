import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import calendar
import os

def read_and_prepare_data(file_path, date_col, load_col, months=None):
    data = pd.read_csv(file_path)
    data[date_col] = pd.to_datetime(data[date_col].str.split(' - ').str[0], dayfirst=True)
    data.set_index(date_col, inplace=True)
    
    if months is not None:
        data = data[data.index.month.isin(months)]
        
    return data

def rank_demanding_months(data, months):
    demanding_months_ranked = {}
    for label, df in data.items():
        df = df[df.index.month.isin(months)]
        monthly_mean = df.resample('ME').mean()
        ranked_months = monthly_mean.sort_values(by=load_column, ascending=False)
        demanding_months_ranked[label] = [calendar.month_name[month] for month in ranked_months.index.month]
    return demanding_months_ranked

def plot_data(data, months, plot_title, output_file, colors):
    bar_width = 0.35
    indices = np.arange(len(months))
    plt.figure(figsize=(14, 7))

    for i, (label, df) in enumerate(data.items()):
        # Generate a full date range for the months we're interested in
        full_date_range = pd.date_range(start=df.index.min(), periods=12, freq='MS')
        full_months_df = pd.DataFrame(index=full_date_range).join(df, how='left')
        monthly_data = full_months_df.resample('ME').mean()
        monthly_data_filtered = monthly_data[monthly_data.index.month.isin(months)].fillna(0)
        plt.bar(indices + i * bar_width, monthly_data_filtered[load_column], label=label, width=bar_width, color=colors[i % len(colors)])

    plt.title(plot_title)
    plt.xlabel('Month')
    plt.ylabel('Average Load (MW)')
    plt.xticks(indices + bar_width / 2, [calendar.month_name[month] for month in months], rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

def main(file_paths, months_to_plot, date_column, load_column, plot_title, output_dir, colors):
    data_combined = {}
    for file_path in file_paths:
        country_name = os.path.basename(file_path).split('.')[0]
        data_combined[country_name] = read_and_prepare_data(file_path, date_column, load_column, months=months_to_plot)
    
    ranked_months = rank_demanding_months(data_combined, months_to_plot)
    for label, ranked_list in ranked_months.items():
        print(f"The most energy-demanding months for {label} are:", ', '.join(ranked_list) + '.')

    output_file = os.path.join(output_dir, 'Spain_Comparison.png')
    plot_data(data_combined, months_to_plot, plot_title, output_file, colors)

# Example usage
months_to_plot = [1, 2, 3, 10, 11, 12]
file_paths = [
    '/Users/glyts/Documents/GitHub/Illuminator/Penelope/CSV/Spain2022.csv',
    '/Users/glyts/Documents/GitHub/Illuminator/Penelope/CSV/Spain2023.csv'
]
date_column = 'Time (CET/CEST)'
load_column = 'Actual Total Load [MW] - Spain (ES)'
plot_title = 'Monthly Load Data Comparison'
output_dir = '/Users/glyts/Documents/GitHub/Illuminator/Penelope/Images'  # Adjusted for the sandbox environment
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

main(file_paths, months_to_plot, date_column, load_column, plot_title, output_dir, colors)

print('\n Version 3.1Beta. Process Completed. Plot Generated.\n')