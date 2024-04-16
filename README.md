# Data Analysis and Visualization Toolkit

This repository contains a Python script that provides tools for data loading, cleaning, and visualization, particularly focusing on disaster data analysis. The toolkit is designed to handle CSV data files, perform preliminary data inspections, clean the data and generate several types of plots.

## Features

- **Data Loading**: Load CSV files with customizable parameters for separators, encoding, and headers.
- **Initial Data Inspection**: Get a quick overview of the data including size, basic info, and statistical summaries.
- **Data Cleaning**: Remove columns with high percentages of missing values and save cleaned data.
- **Frequency Analysis**: Calculate the frequency of occurrences for specified columns.
- **Plotting**: Generate bar charts, heatmaps, and line plots to visualize data distributions and trends.

## Installation

To run this script, you need Python installed on your system along with the following Python libraries:
- Pandas
- NumPy
- Matplotlib
- Seaborn

You can install these packages using pip:

```bash
pip install pandas numpy matplotlib seaborn
```

## Usage

To use this toolkit, follow these steps:

1. Clone the Repository:
```bash
git clone https://github.com/Valenwr/Disasters.git
```
2. Navigate to the Project Directory:
```bash
cd Disasters
python Disasters.py
```
## Functions Overview
- **load_data(file_path, sep, encoding='latin-1', header=0)**: Load data from specified CSV file.
- **initial_inspection(data)**: Conduct a preliminary inspection of the loaded data.
- **data_cleaning(data, missing_threshold=10, save_original=False, ...)**: Clean the dataset based on defined criteria for missing data.
- **frequency(data, column_name)**: Compute frequency distributions for a specific column.
- **plotter_disaster_frequency(frequency_dict, x_name, y_name, title, save_path)**: Visualize frequency distributions using bar charts.
- **plotter_disasters_heatmap(...)**: Create heatmaps for exploring relationships between different data dimensions.
