import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

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

def main():
    # Check the base path
    base_path = os.path.dirname(os.path.abspath(__file__))
    print("Base Path:", base_path)

    # Construct the full path to the file
    file_path = os.path.join(base_path, "public_emdat_custom_request_2024-08-23.csv")
    print("Full Path to File:", file_path)

    # Check if the file exists
    if os.path.exists(file_path):
        print("File exists.")
    else:
        print("File does not exist. Check the path and file name.")

    # Load the data
    data_disasters = load_data(file_path, sep=';', encoding='latin-1', header=0)

    data = initial_inspection(data_disasters)
    data_cleaning(data, 10, False, original_filename='data_all_columns.csv', cleaned_filename='data_columns_cleaned.csv')

if __name__ == "__main__":
    main()
