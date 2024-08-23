import streamlit as st
import pandas as pd
import plotly.express as px
from Disasters import data_processing, visualization

st.set_page_config(layout="wide", page_title="Disaster Data Analysis")

st.title("Disaster Data Analysis Toolkit")

# Sidebar for navigation
page = st.sidebar.selectbox("Choose a page", ["Overview", "Time Series", "Geospatial", "Statistics"])

# Load and process data
@st.cache_data
def load_data():
    # Use your data loading and processing functions here
    return data_processing.load_and_process_data()

data = load_data()

if page == "Overview":
    st.write("Welcome to the Disaster Data Analysis Toolkit. Choose a page from the sidebar to explore different visualizations.")

elif page == "Time Series":
    st.header("Disaster Occurrences Over Time")
    
    # Time range selector
    date_range = st.date_input("Select date range", [data['date'].min(), data['date'].max()])
    
    # Filter data based on selected date range
    filtered_data = data[(data['date'] >= date_range[0]) & (data['date'] <= date_range[1])]
    
    # Create time series plot
    fig = px.line(filtered_data, x='date', y='occurrences', title='Disaster Occurrences Over Time')
    st.plotly_chart(fig, use_container_width=True)

elif page == "Geospatial":
    st.header("Geospatial Distribution of Disasters")
    
    # Create map
    fig = px.scatter_mapbox(data, lat='latitude', lon='longitude', color='disaster_type',
                            zoom=3, height=500)
    fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Statistics":
    st.header("Disaster Statistics")
    
    # Create bar chart of disaster types
    fig = px.bar(data['disaster_type'].value_counts(), title='Disaster Types')
    st.plotly_chart(fig, use_container_width=True)

# Add more visualizations and interactivity as needed