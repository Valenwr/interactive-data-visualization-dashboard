# Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from graphfunctions import load_data

color_palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

# Function to plot the distribution of disaster groups
def plot_disaster_group_distribution(data):
    group_data = data['Disaster Group'].value_counts()
    fig = px.pie(values=group_data.values, names=group_data.index,
                 title='Distribution of Disaster Groups',
                 color_discrete_sequence=color_palette)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# Function to plot the top N most frequent disaster types
def plot_top_disaster_types(data, n=10):
    top_disasters = data['Disaster Type'].value_counts().nlargest(n)
    fig = px.bar(x=top_disasters.index, y=top_disasters.values,
                 labels={'x':'Disaster Type', 'y':'Count'},
                 title=f'Top {n} Most Frequent Disaster Types',
                 color=top_disasters.index,
                 color_discrete_sequence=color_palette)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title_font=dict(size=14),
        yaxis_title_font=dict(size=14)
    )
    return fig

# Function to plot the yearly trend of disaster occurrences
def plot_yearly_trend(data):
    yearly_data = data.groupby('Start Year').size().reset_index(name='Count')
    fig = px.line(yearly_data, x='Start Year', y='Count',
                  title='Yearly Trend of Disaster Occurrences')
    fig.update_traces(line_color=color_palette[0], line_width=3)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title_font=dict(size=14),
        yaxis_title_font=dict(size=14)        
    )
    return fig

# Function to plot the monthly distribution of disasters using a polar chart
def plot_monthly_distribution(data):
    monthly_data = data['Start Month'].value_counts().sort_index()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=monthly_data.values,
        theta=months,
        mode='lines+markers',
        name='Disasters',
        line=dict(color=color_palette[0], width=3),
        marker=dict(color=color_palette[1], size=10),
        fill='toself',
        fillcolor=color_palette[2]
    ))

    fig.update_layout(
        title={
            'text': 'Monthly Distribution of Disasters',
            'font': {'size': 24}
        },
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(monthly_data.values)],
                showline=False,
                showticklabels=False,
            ),
            angularaxis=dict(
                direction="clockwise",
                period=12
            )
        ),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    # Add value annotations
    for i, value in enumerate(monthly_data.values):
        angle = (i / 12) * 2 * 3.14159  # convert to radians
        r = value
        x = r * np.cos(angle)
        y = r * np.sin(angle)
        fig.add_annotation(
            x=x, y=y,
            text=str(value),
            showarrow=False,
            font=dict(size=10, color="black")
        )

    return fig
# Function to plot the occurrences of disaster subgroups
def plot_disaster_subgroup_occurrences(data):
    subgroup_data = data['Disaster Subgroup'].value_counts()
    fig = px.bar(x=subgroup_data.index, y=subgroup_data.values,
                 labels={'x':'Disaster Subgroup', 'y':'Count'},
                 title='Occurrences of Disaster Subgroups',
                 color=subgroup_data.index,  # Assign different colors to each bar
                 color_discrete_sequence=color_palette)  # Use our custom color palette
    
    fig.update_layout(
        xaxis={'categoryorder':'total descending',
               'title_font': {'size': 14},
               'tickangle': -45},  # Rotate x-axis labels for better readability
        yaxis={'title_font': {'size': 14}},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        bargap=0.2,  # Adjust the gap between bars
        height=500,  # Adjust the height of the chart for better visibility
        margin=dict(l=50, r=50, t=50, b=100)  # Adjust margins
    )
    
    # Customize hover information
    fig.update_traces(hovertemplate='Subgroup: %{x}<br>Count: %{y}')
    
    # Add value labels on top of each bar
    fig.update_traces(texttemplate='%{y}', textposition='outside')

    return fig

# Function to plot the distribution of disaster types
def plot_disaster_types_distribution(data):
    type_data = data['Disaster Type'].value_counts()
    fig = px.bar(x=type_data.index, y=type_data.values,
                 labels={'x':'Disaster Type', 'y':'Count'},
                 title='Bar Chart of Disaster Types Distribution',
                 color=type_data.index,
                 color_discrete_sequence=color_palette)
    fig.update_layout(
        xaxis={'categoryorder':'total descending',
               'title_font': {'size': 14},
               'tickangle': -45},  # Rotate x-axis labels for better readability
        yaxis={'title_font': {'size': 14}},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        bargap=0.2,  # Adjust the gap between bars
        height=600,  # Increase the height of the chart for better visibility
        margin=dict(b=100)  # Increase bottom margin to accommodate rotated labels
    )
    
    # Customize hover information
    fig.update_traces(hovertemplate='Disaster Type: %{x}<br>Count: %{y}')
    return fig

# Function to create a heatmap of disaster occurrences by type and month
def plot_heatmap_type_month(data):
    heatmap_data = pd.crosstab(data['Start Month'], data['Disaster Type'])
    fig = px.imshow(heatmap_data,
                    labels=dict(x="Disaster Type", y="Month", color="Count"),
                    title="Heatmap of Disaster Occurrences by Type and Month")
    fig.update_layout(xaxis={'categoryorder':'total ascending'})
    return fig

# Function to plot the monthly distribution of disasters using a bar chart
def plot_monthly_distribution_bar(data):
    monthly_data = data['Start Month'].value_counts().sort_index()
    fig = px.bar(x=monthly_data.index, y=monthly_data.values,
                 labels={'x':'Month', 'y':'Count'},
                 title='Monthly Distribution of Disasters',
                 color=monthly_data.index,
                 color_discrete_sequence=color_palette)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title_font=dict(size=14),
        yaxis_title_font=dict(size=14),
        bargap=0.2  # Adjust the gap between bars
    )
    # Customize the hover information
    fig.update_traces(hovertemplate='Month: %{x}<br>Count: %{y}')
    return fig

# Function to plot the OFDA/BHA response distribution using a donut chart
def plot_response_comparison(data):
    response_data = data['OFDA/BHA Response'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=response_data.index,
        values=response_data.values,
        hole=.3,  # This creates the donut hole
        textinfo='label+percent',
        insidetextorientation='radial',
        marker=dict(colors=color_palette)
    )])
    
    fig.update_layout(
        title_text='OFDA/BHA Response Distribution',
        annotations=[dict(text='', x=0.5, y=0.5, font_size=20, showarrow=False)]
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
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

    # Set the background color
    st.markdown(
        """
        <style>
        .stApp{
        background-color: #FFFFFF;
        }        
        """,
        unsafe_allow_html=True
    )
    # Set the title and logo
    st.title("🌪️ Disaster Analysis Dashboard")
    st.sidebar.image("https://www.example.com/your_logo.png", width=200)

    # Load the data
    data_clean = load_data(r'C:\Users\Valentina\Desktop\Proyectos\Disasters\data-clean.csv', sep=',', encoding='latin-1', header=0)

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

    # Apply filters to the data
    filtered_data = data_clean[
        (data_clean['Start Year'].between(selected_years[0], selected_years[1])) &
        (data_clean['Region'].isin(selected_regions))
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
        st.subheader("Yearly Trend of Disaster Occurrences")
        fig_trend = plot_yearly_trend(filtered_data)
        st.plotly_chart(fig_trend, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Monthly Distribution (Polar)")
            fig_monthly = plot_monthly_distribution(filtered_data)
            st.plotly_chart(fig_monthly, use_container_width=True)
        with col2:
            st.subheader("Monthly Distribution (Bar)")
            fig_monthly_bar = plot_monthly_distribution_bar(filtered_data)
            st.plotly_chart(fig_monthly_bar, use_container_width=True)

        st.subheader("Heatmap of Disaster Occurrences by Type and Month")
        fig_heatmap_type_month = plot_heatmap_type_month(filtered_data)
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