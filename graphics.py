# Import necessary libraries
import streamlit as st
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from graphfunctions import load_data

# Function to plot the distribution of disaster groups
def plot_disaster_group_distribution(data):
    group_data = data['Disaster Group'].value_counts()
    fig = px.pie(values=group_data.values, names=group_data.index,
                 title='Distribution of Disaster Groups')
    return fig

# Function to plot the top N most frequent disaster types
def plot_top_disaster_types(data, n=10):
    top_disasters = data['Disaster Type'].value_counts().nlargest(n)
    fig = px.bar(x=top_disasters.index, y=top_disasters.values,
                 labels={'x':'Disaster Type', 'y':'Count'},
                 title=f'Top {n} Most Frequent Disaster Types')
    return fig

# Function to plot the yearly trend of disaster occurrences
def plot_yearly_trend(data):
    yearly_data = data.groupby('Start Year').size().reset_index(name='Count')
    fig = px.line(yearly_data, x='Start Year', y='Count',
                  title='Yearly Trend of Disaster Occurrences')
    return fig

# Function to plot the monthly distribution of disasters using a polar chart
def plot_monthly_distribution(data):
    monthly_data = data['Start Month'].value_counts().sort_index()
    fig = px.line_polar(r=monthly_data.values, theta=monthly_data.index, line_close=True,
                        title='Monthly Distribution of Disasters')
    return fig

# Function to plot the occurrences of disaster subgroups
def plot_disaster_subgroup_occurrences(data):
    subgroup_data = data['Disaster Subgroup'].value_counts()
    fig = px.bar(x=subgroup_data.index, y=subgroup_data.values,
                 labels={'x':'Disaster Subgroup', 'y':'Count'},
                 title='Bar Chart of Disaster Subgroup Occurrences')
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    return fig

# Function to plot the distribution of disaster types
def plot_disaster_types_distribution(data):
    type_data = data['Disaster Type'].value_counts()
    fig = px.bar(x=type_data.index, y=type_data.values,
                 labels={'x':'Disaster Type', 'y':'Count'},
                 title='Bar Chart of Disaster Types Distribution')
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    return fig

def plot_complex_disaster_bubble_chart(data, selected_disaster_groups, selected_regions):
    # Filter the data based on selected disaster groups and regions
    filtered_data = data[
        (data['Disaster Group'].isin(selected_disaster_groups)) &
        (data['Region'].isin(selected_regions))
    ]
    
    # Prepare the data
    summary_data = filtered_data.groupby(['Disaster Group', 'Start Month', 'Region']).agg({
        'DisNo': 'count',
        'Start Year': 'min',
        'End Year': 'max',
        'OFDA/BHA Response': lambda x: x.notna().sum(),
        'Appeal': lambda x: x.notna().sum(),
        'Declaration': lambda x: x.notna().sum()
    }).reset_index()
    
    summary_data.columns = ['Disaster Group', 'Month', 'Region', 'Count', 'First Occurrence', 'Last Occurrence', 'OFDA Responses', 'Appeals', 'Declarations']
    
    # Calculate a composite 'Impact Score'
    summary_data['Impact Score'] = summary_data['OFDA Responses'] + summary_data['Appeals'] + summary_data['Declarations']
    
    # Create the bubble chart
    fig = px.scatter(summary_data, 
                     x='Month', 
                     y='Disaster Group', 
                     size='Count',
                     color='Region',
                     hover_name='Disaster Group',
                     hover_data=['Count', 'First Occurrence', 'Last Occurrence', 'OFDA Responses', 'Appeals', 'Declarations', 'Impact Score'],
                     title="Complex Bubble Chart of Disaster Occurrences",
                     color_discrete_sequence=px.colors.qualitative.Prism)
    
    # Customize the layout
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Disaster Group",
        xaxis=dict(tickmode='linear', tick0=1, dtick=1),
        yaxis={'categoryorder':'total descending'},
        legend_title="Region"
    )
    
    # Adjust bubble size for better visibility
    fig.update_traces(marker=dict(sizemode='area', sizeref=2.*max(summary_data['Count'])/(40.**2), sizemin=4))
    
    # Add custom hover template
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>" +
        "Month: %{x}<br>" +
        "Count: %{marker.size}<br>" +
        "Region: %{color}<br>" +
        "First Occurrence: %{customdata[1]}<br>" +
        "Last Occurrence: %{customdata[2]}<br>" +
        "OFDA Responses: %{customdata[3]}<br>" +
        "Appeals: %{customdata[4]}<br>" +
        "Declarations: %{customdata[5]}<br>" +
        "Impact Score: %{customdata[6]}<extra></extra>"
    )
    
    return fig

# Function to plot the monthly distribution of disasters using a bar chart
def plot_monthly_distribution_bar(data):
    monthly_data = data['Start Month'].value_counts().sort_index()
    fig = px.bar(x=monthly_data.index, y=monthly_data.values,
                 labels={'x':'Month', 'y':'Count'},
                 title='Monthly Distribution of Disasters')
    return fig

# Function to plot the OFDA/BHA response distribution using a donut chart
def plot_response_comparison(data):
    response_data = data['OFDA/BHA Response'].value_counts().reset_index()
    response_data.columns = ['Response', 'Count']
    
    # Calculate percentages
    total = response_data['Count'].sum()
    response_data['Percentage'] = response_data['Count'] / total * 100
    
    # Sort so 'No' comes first
    response_data = response_data.sort_values('Response', ascending=False)

    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=response_data['Response'],
        y=response_data['Percentage'],
        textposition='auto',
        marker_color=['#1f77b4', '#ff7f0e']  # Use two contrasting colors
    ))

    fig.update_layout(
        title='OFDA/BHA Response Distribution',
        xaxis_title='Response',
        yaxis_title='Percentage',
        yaxis=dict(tickformat='.1f', ticksuffix='%'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )

    return fig

# Function to create a choropleth map
def make_choropleth(input_df, input_column, input_color_theme):
    choropleth = px.choropleth(input_df, 
                               locations='ISO', 
                               color=input_column, 
                               color_continuous_scale=input_color_theme,
                               range_color=(0, input_df[input_column].max()),
                               scope="world",
                               labels={input_column: input_column}
                              )
    choropleth.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=500
    )
    return choropleth

# Main function to run the Streamlit app
def main():
    # Set up the page configuration
    st.set_page_config(page_title="Disaster Analysis Dashboard", page_icon="📊", layout="wide")

    # Set the title and logo
    st.title("📊 Disaster Analysis Dashboard")

    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "data-clean.csv")

    # Load the data
    data_clean = load_data(file_path, sep=',', encoding='latin-1', header=0)

    # Sidebar filters
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

    # Apply filters to the data
    filtered_data = data_clean[
        (data_clean['Start Year'].between(selected_years[0], selected_years[1])) &
        (data_clean['Region'].isin(selected_regions)) &
        (data_clean['Disaster Group'].isin(selected_disaster_groups))
    ]

    # Create tabs for different sections of the dashboard
    tab1, tab2, tab3 = st.tabs(["Overview", "Temporal Analysis", "Choropleth Map"])

    # Tab 1: Overview
    with tab1:
        st.header("Disaster Overview")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Disaster Group Distribution")
            fig_group = plot_disaster_group_distribution(filtered_data)
            st.plotly_chart(fig_group, use_container_width=True)
        with col2:
            st.subheader("Top Disaster Types")
            fig_top = plot_top_disaster_types(filtered_data)
            st.plotly_chart(fig_top, use_container_width=True)

        st.subheader("OFDA/BHA Response Distribution")
        fig_response = plot_response_comparison(filtered_data)
        st.plotly_chart(fig_response, use_container_width=True)

    # Tab 2: Temporal Analysis
    with tab2:
        st.header("Temporal Analysis")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Yearly Trend of Disaster Occurrences")
            fig_trend = plot_yearly_trend(filtered_data)
            st.plotly_chart(fig_trend, use_container_width=True)
        with col2:
            st.subheader("Monthly Distribution (Bar)")
            fig_monthly_bar = plot_monthly_distribution_bar(filtered_data)
            st.plotly_chart(fig_monthly_bar, use_container_width=True)

        st.subheader("Heatmap of Disaster Occurrences by Type and Month")
        fig_heatmap_type_month = plot_complex_disaster_bubble_chart(filtered_data, selected_disaster_groups, selected_regions)
        st.plotly_chart(fig_heatmap_type_month, use_container_width=True)

    # Tab 3: Choropleth Map
    with tab3:
        st.header("Choropleth Map")
        
        # Prepare data for choropleth
        choropleth_data = filtered_data.groupby('ISO').size().reset_index(name='Disaster Count')
        
        # Color theme selection
        color_theme = st.selectbox("Select Color Theme", 
                                    ["Viridis", "Plasma", "Inferno", "Magma", "Cividis"])
        
        # Create and display choropleth map
        fig_choropleth = make_choropleth(choropleth_data, 'Disaster Count', color_theme)
        st.plotly_chart(fig_choropleth, use_container_width=True)

    # Footer
    st.markdown("---")
    st.markdown("Dashboard created with ❤️ using Streamlit")

# Run the main function when the script is executed
if __name__ == "__main__":
    main()