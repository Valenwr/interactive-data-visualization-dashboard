# Disaster Analysis Dashboard

An interactive dashboard for analyzing and visualizing disaster-related datasets. This dashboard allows users to explore disaster data by visualizing distributions, trends, and spatial patterns interactively, using a clean and user-friendly interface powered by Streamlit and Plotly.

## Features

- **Interactive Data Visualization**: Create interactive plots including pie charts, bar charts, line charts, treemaps, and choropleth maps to explore different aspects of disaster data.
- **Dynamic Filtering**: Use sidebar controls to filter data by year range, regions, and disaster groups.
- **Temporal Analysis**: Visualize yearly trends and monthly distributions of disaster occurrences.
- **Spatial Analysis**: Generate choropleth maps to display the distribution of disasters across different regions.
- **User-Friendly Interface**: Built with Streamlit, allowing for a responsive and easy-to-navigate dashboard.

## Technologies Used

- **Streamlit**: For creating a web-based interactive user interface.
- **Plotly**: For generating dynamic and interactive visualizations.
- **Pandas**: For data manipulation and processing.
- **Python**: Core programming language for data analysis and visualization.

## Installation

To run this application, you need to have Python installed on your system along with the required libraries. 

### Prerequisites

Ensure you have the following Python libraries installed:

- `streamlit`
- `plotly`
- `pandas`

Install the required packages using pip:

```bash
pip install streamlit plotly pandas
```

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/disaster-analysis-dashboard.git
   ```

2. Navigate to the project directory:
   ```bash
   cd disaster-analysis-dashboard
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Load Data**: The app loads data from `data-clean.csv` located in the project directory. Ensure this file is correctly formatted with columns such as 'Disaster Group', 'Disaster Type', 'Start Year', 'Start Month', 'Region', 'ISO', etc.
2. **Filter Data**: Use the sidebar to select the year range, regions, and disaster groups for analysis.
3. **Explore Visualizations**: Use the tabs to switch between different types of visualizations:
   - Overview: View the distribution of disaster groups, top disaster types, and disaster subtypes.
   - Temporal Analysis: Analyze trends over time with yearly and monthly visualizations.
   - Spatial Analysis: Examine geographical patterns of disasters using choropleth maps and country-specific data.

## Dashboard Features

### Plotting Functions

- `plot_disaster_group_distribution(data)`: Creates a pie chart of the distribution of disaster groups.
- `plot_top_disaster_types(data, n=10)`: Generates a bar chart of the top N most frequent disaster types.
- `plot_yearly_trend(data)`: Plots a line chart showing the yearly trend of disaster occurrences.
- `plot_monthly_distribution(data)`: Displays a bar chart for the monthly distribution of disasters.
- `plot_disaster_subtypes(data)`: Creates a treemap showing the distribution of disaster subtypes.
- `make_choropleth(input_df, input_column, input_color_theme)`: Generates a choropleth map based on selected data.

### Tabs

1. **Overview**: Provides a summary of disaster distributions.
2. **Temporal Analysis**: Focuses on disaster trends over time.
3. **Spatial Analysis**: Analyzes geographical distribution and impact.

## Deployment

You can deploy this dashboard to any hosting service that supports Python, such as Heroku or AWS. To deploy:

1. Commit your changes to the repository.
2. Follow platform-specific deployment instructions.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a branch for your changes
3. Make your changes and commit them
4. Submit a pull request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

- Data is sourced from the [EM-DAT database](https://www.emdat.be/), provided by the Centre for Research on the Epidemiology of Disasters (CRED).
- Thanks to the Streamlit and Plotly communities for their excellent documentation and examples.
