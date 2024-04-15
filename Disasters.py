import pandas as pd
import geopandas
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import os
import sys

def load_data(file_path, sep, encoding='latin-1', header=0):
    """
    Load data from a CSV file.
    """
    try:
        data = pd.read_csv(file_path, sep=sep, encoding=encoding, low_memory=False, header=header)
        print(f"Data loaded successfully with {data.shape[0]} rows and {data.shape[1]} columns.")
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        raise
    except Exception as e:
        print(f"An error occurred while loading the data: {e}")
        raise
    return data

def initial_inspection(data):
    '''
    Made an initial inspection of the database.
    '''
    pd.set_option('display.max_columns', 500)
    '''
    # Size of Data
    num_rows, num_cols = data.shape
    print('The data has {} rows and {} columns'.format(num_rows, num_cols))
    print('')
    
    # Basic info
    print(data.info())
    print('')
    
    # First look at data
    print(data.tail())
    print('')
    
    # To get a descriptive statical overview
    """
    count: the number of non-null entries
    mean: the mean value
    std: the standard deviation
    min: the minimum value
    25%, 505, 75%: the lower, median, and upper quartiles
    max: the maximum value
    """
    print(data.describe())
    print('')

    # To check is the data has any missing values
    print(data.isnull().any())
    print('Percentage of Missing Values: ')
    print(data.isnull().sum()/data.shape[0]*100)
    '''
    # Check for duplicates entries 
    # print(data.duplicated())

    # Dataframe with only unique rows
    data = data.drop_duplicates()

    return data

def data_cleaning(data, missing_threshold=10, save_original=False, original_filename='data_all_columns.csv', cleaned_filename='data_columns_cleaned.csv'):
    """
    Clean the data by removing columns with a high percentage of missing values.

    Parameters:
        data (pd.DataFrame): DataFrame to clean.
        missing_threshold (float): Percentage threshold for missing values to drop the column.
        save_original (bool): Whether to save the original data to a CSV.
        original_filename (str): Filename for saving the original data.
        cleaned_filename (str): Filename for saving the cleaned data.

    Returns:
        pd.DataFrame: Cleaned DataFrame with columns dropped based on the missing values threshold.
    """
    print('Cleaning data...')
    cleaned_data = data.copy()

    if save_original:
        data.to_csv(original_filename, index=False, encoding='utf-8')

    # Calculate the percentage of missing values for each column
    missing_percentage = cleaned_data.isnull().mean() * 100

    # Identify columns where the percentage of missing values is greater than the threshold
    columns_to_drop = missing_percentage[missing_percentage > missing_threshold].index
    cleaned_data.drop(columns=columns_to_drop, inplace=True)

    # Log the columns dropped
    print(f"Dropped {len(columns_to_drop)} columns with more than {missing_threshold}% missing values.")

    cleaned_data.to_csv(cleaned_filename, index=False, encoding='utf-8')

    return cleaned_data

def frequency(data, column_name):
    """
    Calculates the frequency of an event.
    """
    value_counts = data[column_name].value_counts()
    # Convert the Series to a dictionary
    frequency_dict = value_counts.to_dict()
    
    return frequency_dict

def frequency_response(data,  response, region_column, column_name='OFDA/BHA Response'):
    # Filter the data for response
    yes_responses = data[data[column_name] == response]

    # Count the number of responses in each region
    yes_counts_by_region = yes_responses[region_column].value_counts()

    # Convert the Series to a dictionary
    frequency_dict = yes_counts_by_region.to_dict()

    return frequency_dict

def plotter_disaster_frequency(frequency_dict, x_name, y_name, title):
    """
    Plot the frequency distribution from a dictionary containing disaster data.

    Parameters:
        frequency_dict (dict): Dictionary with categories as keys and frequencies as values.
        x_label (str): Label for the x-axis, representing the category of data.
        y_label (str): Label for the y-axis, representing the frequency of occurrences.
        title (str): Title of the plot.

    Description:
        This function creates a bar chart visualizing the frequency of different disaster types or categories,
        which is helpful for quick graphical analysis of data distributions.
    """
    # Prepare data for plotting
    categories = list(frequency_dict.keys())
    frequencies = list(frequency_dict.values())

    # Set a style
    plt.style.use('_mpl-gallery') # or ''_mpl-gallery', 'dark_background', 'ggplot', 'grayscale', 'seaborn-v0_8'

    # Creating the bar chart
    plt.figure(figsize=(14, 8))
    bars = plt.bar(categories, frequencies, color=plt.cm.Paired(range(len(categories))), edgecolor='black')
    
    # Adding value labels on top of each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 1), ha='center', va='bottom', fontweight='bold')
    
    # Add labels and title
    plt.xlabel(x_name, fontsize=12, fontweight='bold')
    plt.ylabel(y_name, fontsize=12, fontweight='bold')
    plt.title(title, fontsize=14, fontweight='bold')

    # Add grid for better readability of the plot
    plt.grid(True, color='grey', linestyle=':', linewidth=0.5, alpha=0.7)
    
    # Display the plot
    plt.tight_layout()
    
    # Automatically format x-axis labels to fit the plot
    plt.gcf().autofmt_xdate()

    plt.show()  

def plotter_disasters_heatmap(data, index_col, columns_col, x_label, y_label, title, cmap='viridis', annot=True, fmt='d'):
    """
    Generates and displays a heatmap for the given dataset, handling data preparation including cleaning and transformation.

    Parameters:
        data (pd.DataFrame): The original DataFrame to process.
        index_col (str): The name of the column to use as the index in the heatmap.
        columns_col (str): The name of the column to use as the columns in the heatmap.
        x_label (str): Label for the X-axis.
        y_label (str): Label for the Y-axis.
        title (str): Title of the heatmap.
        cmap (str): Color map for the heatmap.
        annot (bool): Whether to annotate each cell with the integer data.
        fmt (str): Format of the annotation text.

    Returns:
        None: This function only displays a plot.
    """
    # Ensure the relevant columns exist
    if index_col not in data.columns or columns_col not in data.columns:
        raise ValueError("Specified columns are not in the dataframe.")
   
    # Remove rows where the index column is missing and ensure it is of type integer
    cleaned_data = data.dropna(subset=[index_col])
    cleaned_data[index_col] = cleaned_data[index_col].astype(int)

    # Create a cross-tabulation of the specified columns
    data_cross_tab = pd.crosstab(cleaned_data[index_col], cleaned_data[columns_col])

    # Plotting the heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(data_cross_tab, cmap=cmap, annot=annot, fmt=fmt)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)  # keep the month labels horizontal for readability
    plt.tight_layout()  # adjusts plot to fit labels

    plt.show()

def occurrences_over_the_years(data, column_name):
    """
    Plot the occurrence of events over the years specified in a given column.

    Parameters:
        data (pd.DataFrame): The DataFrame containing the data.
        column_name (str): The column name that contains the year data.

    Returns:
        None: The function plots the occurrences per year.
    """
    if column_name not in data.columns:
        raise ValueError(f"The column '{column_name}' does not exist in the DataFrame.")

    # Group data by the specified column and count occurrences
    disaster_counts = data.groupby(column_name).size()
    print('disaster_counts: ', disaster_counts)

    # Sorting the data by year, although groupby and size should inherently maintain order
    disaster_counts = disaster_counts.sort_index()
    print('disaster_counts_2": ', disaster_counts)

    # Setting up the plot
    plt.figure(figsize=(10, 6))
    plt.plot(disaster_counts.index, disaster_counts.values, marker='o', linestyle='-', color='blue')
    plt.title('Number of Disasters per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Disasters')
    plt.grid(True)  # Adding a grid for better readability
    plt.tight_layout()  # Adjusts plot to fit labels

    plt.show()

def plot_grouped_bar_chart(yes, no, style='default', title='Frequency of Responses by Region',
                           colors=('blue', 'orange'), bar_width=0.35, figsize=(14, 8)):
    """
    Plots a grouped bar chart with 'Yes' and 'No' response frequencies by region.

    Parameters:
        yes (dict): Dictionary with regions as keys and 'Yes' counts as values.
        no (dict): Dictionary with regions as keys and 'No' counts as values.
        style (str): Matplotlib style to use for plotting.
        title (str): Title of the chart.
        colors (tuple): Colors for the 'Yes' and 'No' bars.
        bar_width (float): Width of each bar.
        figsize (tuple): Dimensions of the figure.
    """
    # Activate the specified matplotlib style
    plt.style.use(style)

    # Prepare the data
    regions = list(yes.keys())
    yes_counts = [yes[region] for region in regions]
    no_counts = [no[region] for region in regions]

    # Create figure and axis objects
    fig, ax = plt.subplots(figsize=figsize)

    # Calculate the positions for the bars
    index = np.arange(len(regions))
    bar_positions1 = index - bar_width / 2
    bar_positions2 = index + bar_width / 2

    # Plot the bars for 'Yes' and 'No' responses
    bars1 = ax.bar(bar_positions1, yes_counts, bar_width, label='Yes Responses', color=colors[0], edgecolor='black')
    bars2 = ax.bar(bar_positions2, no_counts, bar_width, label='No Responses', color=colors[1], edgecolor='black')

    # Add value labels on top of each bar
    def add_value_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height, round(height, 1),
                    ha='center', va='bottom', fontweight='bold')

    add_value_labels(bars1)
    add_value_labels(bars2)

    # Set up the axes, labels, title, and legend
    ax.set_xlabel('Region', fontsize=12, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xticks(index)
    ax.set_xticklabels(regions)
    ax.grid(True, color='grey', linestyle=':', linewidth=0.5, alpha=0.7)
    ax.legend()

    # Layout adjustment
    plt.tight_layout()
    plt.show()


def main():
    # Check the base path
    base_path = os.path.dirname(os.path.abspath(__file__))
    print("Base Path:", base_path)

    # Construct the full path to the file
    file_path = os.path.join(base_path, "Disasters_1900_2022.csv")
    print("Full Path to File:", file_path)

    # Check if the file exists
    if os.path.exists(file_path):
        print("File exists.")
    else:
        print("File does not exist. Check the path and file name.")

    # Load the data
    data_disasters = load_data(file_path, sep=';', encoding='latin-1', header=0)

    data = initial_inspection(data_disasters)
    data_clean = data_cleaning(data, 10, False, original_filename='data_all_columns.csv', cleaned_filename='data_columns_cleaned.csv')
    
    # Plot the frequency of Disasters Subgroup and Disasters Type / Months
    disaster_frequency_disaster_subgroup = frequency(data_clean, 'Disaster Subgroup')
    plotter_disaster_frequency(frequency_dict=disaster_frequency_disaster_subgroup, x_name='Disaster Types Subgroup', y_name='Frequency', title='Frequency of Disasters Types')
   
    disaster_frequency_disaster_type = frequency(data_clean, 'Disaster Type')
    plotter_disaster_frequency(frequency_dict=disaster_frequency_disaster_type, x_name='Disaster Types', y_name='Frequency', title='Frequency of Disasters Types')
    
    disaster_frequency_disaster_month = frequency(data_clean, 'Start Month')
    plotter_disaster_frequency(disaster_frequency_disaster_month, x_name='Months', y_name='Number of Disasters', title='Number of Disasters per Month')

    # Plot ocurrences over the years since 1900
    occurrences_over_the_years(data_clean, 'Start Year')

    # Show relationships between two variables
    plotter_disasters_heatmap(data_clean, index_col='Start Month', columns_col='Disaster Subgroup', x_label='Disaster Type', y_label='Month', title='Frequency of Disaster Types by Month')
    plotter_disasters_heatmap(data_clean, index_col='Start Year', columns_col='Disaster Subgroup', x_label='Disaster Type', y_label='Years', title='Frequency of Disaster Types by Year', annot=False)

    # Times OFDA/BHA Response by Region
    disaster_frequency_disaster_region_BHA = frequency(data_clean, 'Region')
    plotter_disaster_frequency(frequency_dict=disaster_frequency_disaster_region_BHA, x_name='Responses', y_name='Regions', title='OFDA/BHA Response')

    # Times YES/NO
    disaster_frequency_disaster_region_BHA_yes = frequency_response(data_clean, 'Yes', 'Region')
    disaster_frequency_disaster_region_BHA_no = frequency_response(data_clean, 'No', 'Region')

    print(disaster_frequency_disaster_region_BHA_yes)
    print(disaster_frequency_disaster_region_BHA_no)

    plot_grouped_bar_chart(disaster_frequency_disaster_region_BHA_yes, disaster_frequency_disaster_region_BHA_no)

if __name__ == "__main__":
    main()
