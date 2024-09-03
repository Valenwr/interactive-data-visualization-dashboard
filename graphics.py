import os
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from graphfunctions import load_data

# Function to plot the distribution of disaster groups
def plot_disaster_group_distribution(data):
    # Count the occurrences of each disaster group
    group_data = data['Disaster Group'].value_counts()
    # Create a pie chart using Plotly Express
    fig = px.pie(values=group_data.values, names=group_data.index,
                 title='Distribution of Disaster Groups',
                 color_discrete_sequence=px.colors.sequential.Viridis)
    # Customize the appearance of the pie chart
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

# Function to plot the top N most frequent disaster types
def plot_top_disaster_types(data, n=10):
    # Get the top N disaster types
    top_disasters = data['Disaster Type'].value_counts().nlargest(n)
    # Create a bar chart using Plotly Express
    fig = px.bar(x=top_disasters.index, y=top_disasters.values,
                 labels={'x':'Disaster Type', 'y':'Count'},
                 title=f'Top {n} Most Frequent Disaster Types',
                 color=top_disasters.values,
                 color_continuous_scale=px.colors.sequential.Viridis)
    # Sort the x-axis by total descending
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    return fig

# Function to plot the yearly trend of disaster occurrences
def plot_yearly_trend(data):
    # Group data by year and count occurrences
    yearly_data = data.groupby('Start Year').size().reset_index(name='Count')
    # Create a line chart using Plotly Express
    fig = px.line(yearly_data, x='Start Year', y='Count',
                  title='Yearly Trend of Disaster Occurrences',
                  labels={'Count': 'Number of Disasters'},
                  line_shape='spline', render_mode='svg')
    # Customize the appearance of the line
    fig.update_traces(line=dict(color="#636EFA", width=3))
    # Set hover mode to show all points for a given x-value
    fig.update_layout(hovermode="x unified")
    return fig

# Function to plot the monthly distribution of disasters
def plot_monthly_distribution(data):
    # Count occurrences for each month
    monthly_data = data['Start Month'].value_counts().sort_index()
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    # Create a bar chart using Plotly Express
    fig = px.bar(x=month_names, y=monthly_data.values,
                 labels={'x':'Month', 'y':'Count'},
                 title='Monthly Distribution of Disasters',
                 color=monthly_data.values,
                 color_continuous_scale=px.colors.sequential.Viridis)
    return fig

# Function to plot the distribution of disaster subtypes
def plot_disaster_subtypes(data):
    # Get the top 15 disaster subtypes
    subtype_data = data['Disaster Subtype'].value_counts().nlargest(15)
    # Create a treemap using Plotly Express
    fig = px.treemap(names=subtype_data.index, parents=['Disaster Subtype']*len(subtype_data),
                     values=subtype_data.values,
                     title='Distribution of Disaster Subtypes',
                     color=subtype_data.values,
                     color_continuous_scale=px.colors.sequential.Viridis)
    return fig

# Function to create a choropleth map
def make_choropleth(input_df, input_column, input_color_theme):
    # Create a choropleth map using Plotly Express
    choropleth = px.choropleth(input_df, 
                               locations='ISO', 
                               color=input_column, 
                               color_continuous_scale=input_color_theme,
                               range_color=(0, input_df[input_column].max()),
                               scope="world",
                               labels={input_column: input_column})
    # Customize the layout of the map
    choropleth.update_layout(
        geo=dict(showframe=False, showcoastlines=True, projection_type='equirectangular'),
        height=600
    )
    return choropleth

# Main function to run the Streamlit app
def main():
    # Set up the Streamlit page configuration
    st.set_page_config(page_title="Disaster Analysis Dashboard", page_icon="🌪️", layout="wide")

    # Set the title of the dashboard
    st.title("🌪️ Disaster Analysis Dashboard")

    # Load the data
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "data-clean.csv")
    data_clean = load_data(file_path, sep=',', encoding='latin-1', header=0)

    # Create sidebar filters
    st.sidebar.header("Filters")
    selected_years = st.sidebar.slider(
        "Select Year Range",
        min_value=int(data_clean['Start Year'].min()),
        max_value=int(data_clean['Start Year'].max()),
        value=(int(data_clean['Start Year'].min()), int(data_clean['Start Year'].max()))
    )
    selected_regions = st.sidebar.multiselect(
        "Select Regions",
        options=data_clean['Region'].unique(),
        default=data_clean['Region'].unique()
    )
    selected_disaster_groups = st.sidebar.multiselect(
        "Select Disaster Groups",
        options=data_clean['Disaster Group'].unique(),
        default=data_clean['Disaster Group'].unique()
    )

    # Filter the data based on user selections
    filtered_data = data_clean[
        (data_clean['Start Year'].between(selected_years[0], selected_years[1])) &
        (data_clean['Region'].isin(selected_regions)) &
        (data_clean['Disaster Group'].isin(selected_disaster_groups))
    ]

    # Create tabs for different sections of the dashboard
    tab1, tab2, tab3 = st.tabs(["Overview", "Temporal Analysis", "Spatial Analysis"])

    # Tab 1: Overview
    with tab1:
        st.header("Disaster Overview")
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_disaster_group_distribution(filtered_data), use_container_width=True)
        with col2:
            st.plotly_chart(plot_top_disaster_types(filtered_data), use_container_width=True)
        
        st.plotly_chart(plot_disaster_subtypes(filtered_data), use_container_width=True)

    # Tab 2: Temporal Analysis
    with tab2:
        st.header("Temporal Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_yearly_trend(filtered_data), use_container_width=True)
        with col2:
            st.plotly_chart(plot_monthly_distribution(filtered_data), use_container_width=True)

    # Tab 3: Spatial Analysis
    with tab3:
        st.header("Spatial Analysis")
        # Prepare data for choropleth map
        choropleth_data = filtered_data.groupby('ISO').size().reset_index(name='Disaster Count')
        # Allow user to select color theme for the map
        color_theme = st.selectbox("Select Color Theme", 
                                    ["Viridis", "Plasma", "Inferno", "Magma", "Cividis"])
        st.plotly_chart(make_choropleth(choropleth_data, 'Disaster Count', color_theme), use_container_width=True)

        # Create bar chart for top 10 countries by disaster count
        top_countries = filtered_data['Country'].value_counts().nlargest(10)
        fig_top_countries = px.bar(x=top_countries.index, y=top_countries.values,
                                   labels={'x': 'Country', 'y': 'Number of Disasters'},
                                   title='Top 10 Countries by Number of Disasters',
                                   color=top_countries.values,
                                   color_continuous_scale=px.colors.sequential.Viridis)
        st.plotly_chart(fig_top_countries, use_container_width=True)

    # Add footer
    st.markdown("---")
    st.markdown("Dashboard created with ❤️ using Streamlit and Plotly")

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
    