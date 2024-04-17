# Data Analysis and Visualization Toolkit

This Python script is designed to load, clean, analyze, and visualize disaster-related datasets, specifically utilizing data from the EM-DAT database, provided by the Centre for Research on the Epidemiology of Disasters (CRED). This toolkit handles CSV files and includes functionalities for data inspection, cleaning, frequency analysis, and advanced visualizations.

Visit [EM-DAT](https://www.emdat.be/) for more details on the data.

## Features

- **Data Loading**: Load CSV files with customizable parameters for separators, encoding, and headers.
- **Initial Data Inspection**: Get a quick overview of the data including size, basic info, and statistical summaries.
- **Data Cleaning**: Remove columns with high percentages of missing values and save cleaned data.
- **Frequency Analysis**: Calculate the frequency of occurrences for specified columns.
- **Plotting**: Generate and save bar charts, heatmaps, and line plots as `.png` files to visualize data distributions and trends.

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

## Maintaining Compatibility

### Data Updates and Compatibility

The EM-DAT database is regularly updated with new data.

#### Staying Up-to-Date
We strive to keep this toolkit compatible with the latest versions of the EM-DAT database:
- **Check for Updates**: Regularly visit the EM-DAT website or subscribe to their updates to stay informed about new data releases and format changes.
- **Testing New Data**: When new data is released, we recommend testing the data with our scripts before using it extensively. This helps ensure that there are no disruptions due to format changes.

#### What You Can Do
If you encounter issues with new data formats:
- **Report Issues**: Please open an issue in this repository if you find that the script does not handle new data correctly. Include details of the error and, if possible, a snippet of the data format that caused the issue.
- **Contributing Fixes**: If you're able to adapt the script to work with the new data format, consider contributing your changes back to the project through a pull request.

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
- **frequency(data, column_name)**: Calculate the frequencies of each unique value in a specified column. 
- **plotter_disaster_frequency(frequency_dict, x_name, y_name, title, save_path)**: Visualize distributions using bar charts.
- **plotter_disasters_heatmap(...)**: Create heatmaps for exploring relationships between different data dimensions.

## Contributing
Contributions to enhance or expand this toolkit are welcome! Please fork the repository and open a pull request with your improvements, or create an issue to suggest new features or report bugs.

## License
This project is released under the MIT License. For more details, see the LICENSE.md file in the repository.
