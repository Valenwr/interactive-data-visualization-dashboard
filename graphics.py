import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from graphfunctions import load_data, data_cleaning

def plot_disaster_group_distribution(data):
    group_data = data['Disaster Group'].value_counts()
    fig = px.pie(values=group_data.values, names=group_data.index,
                 title='Distribution of Disaster Groups')
    return fig

def plot_top_disaster_types(data, n=10):
    top_disasters = data['Disaster Type'].value_counts().nlargest(n)
    fig = px.bar(x=top_disasters.index, y=top_disasters.values,
                 labels={'x':'Disaster Type', 'y':'Count'},
                 title=f'Top {n} Most Frequent Disaster Types')
    return fig

def plot_yearly_trend(data):
    yearly_data = data.groupby('Start Year').size().reset_index(name='Count')
    fig = px.line(yearly_data, x='Start Year', y='Count',
                  title='Yearly Trend of Disaster Occurrences')
    return fig

def plot_regional_comparison(data):
    regional_data = data.groupby('Region').size().reset_index(name='Count')
    fig = px.bar(regional_data, x='Region', y='Count',
                 title='Number of Disasters by Region')
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    return fig

def plot_monthly_distribution(data):
    monthly_data = data['Start Month'].value_counts().sort_index()
    fig = px.line_polar(r=monthly_data.values, theta=monthly_data.index, line_close=True,
                        title='Monthly Distribution of Disasters')
    return fig

def plot_disaster_subgroup_occurrences(data):
    subgroup_data = data['Disaster Subgroup'].value_counts()
    fig = px.bar(x=subgroup_data.index, y=subgroup_data.values,
                 labels={'x':'Disaster Subgroup', 'y':'Count'},
                 title='Bar Chart of Disaster Subgroup Occurrences')
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    return fig

def plot_disaster_types_distribution(data):
    type_data = data['Disaster Type'].value_counts()
    fig = px.bar(x=type_data.index, y=type_data.values,
                 labels={'x':'Disaster Type', 'y':'Count'},
                 title='Bar Chart of Disaster Types Distribution')
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    return fig

def plot_heatmap_type_month(data):
    heatmap_data = pd.crosstab(data['Start Month'], data['Disaster Type'])
    fig = px.imshow(heatmap_data,
                    labels=dict(x="Disaster Type", y="Month", color="Count"),
                    title="Heatmap of Disaster Occurrences by Type and Month")
    fig.update_layout(xaxis={'categoryorder':'total ascending'})
    return fig

def plot_monthly_distribution_bar(data):
    monthly_data = data['Start Month'].value_counts().sort_index()
    fig = px.bar(x=monthly_data.index, y=monthly_data.values,
                 labels={'x':'Month', 'y':'Count'},
                 title='Monthly Distribution of Disasters')
    return fig

def plot_subgroup_heatmap(data):
    subgroup_data = pd.crosstab(data['Disaster Group'], data['Disaster Subgroup'])
    fig = px.imshow(subgroup_data, 
                    labels=dict(x="Disaster Subgroup", y="Disaster Group", color="Count"),
                    title="Heatmap of Disaster Groups and Subgroups")
    return fig

def plot_response_comparison(data):
    response_data = data['OFDA/BHA Response'].value_counts()
    fig = px.bar(x=response_data.index, y=response_data.values,
                 labels={'x':'OFDA/BHA Response', 'y':'Count'},
                 title='OFDA/BHA Response Distribution')
    return fig

def make_choropleth(input_df, input_column, input_color_theme):
    # Assuming 'ISO' column contains country codes
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

def main():
    st.set_page_config(page_title="Disaster Analysis Dashboard", page_icon="🌪️", layout="wide")

    st.title("🌪️ Disaster Analysis Dashboard")
    st.sidebar.image("https://www.example.com/your_logo.png", width=200)  # Replace with your logo URL

    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
    
    # Replace 'your_file.csv' with the actual name of your CSV file
    file_path = 'public_emdat_incl_hist_2024-08-19.csv'

    # Read the CSV file
    df = pd.read_csv(file_path)
    # Display the dataframe in the Streamlit app
    #st.write(df)

    if uploaded_file is not None:
        data = load_data(uploaded_file, sep=';', encoding='latin-1', header=0)
        data_clean = data_cleaning(data, 10)

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

        # Apply filters
        filtered_data = data_clean[
            (data_clean['Start Year'].between(selected_years[0], selected_years[1])) &
            (data_clean['Region'].isin(selected_regions))
        ]

        # Main content area with tabs
        tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Temporal Analysis", "Geographical Analysis", "Choropleth Map"])

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

            st.subheader("Disaster Groups and Subgroups Heatmap")
            fig_heatmap = plot_subgroup_heatmap(filtered_data)
            st.plotly_chart(fig_heatmap, use_container_width=True)

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

        with tab3:
            st.header("Geographical Analysis")
            st.subheader("Regional Comparison")
            fig_regional = plot_regional_comparison(filtered_data)
            st.plotly_chart(fig_regional, use_container_width=True)

            st.subheader("OFDA/BHA Response Distribution")
            fig_response = plot_response_comparison(filtered_data)
            st.plotly_chart(fig_response, use_container_width=True)

        with tab4:
            st.header("Choropleth Map")
            
            # Prepare data for choropleth
            choropleth_data = filtered_data.groupby('ISO').size().reset_index(name='Disaster Count')
            
            # Color theme selection
            color_theme = st.selectbox("Select Color Theme", 
                                       ["Viridis", "Plasma", "Inferno", "Magma", "Cividis"])
            
            # Create choropleth map
            fig_choropleth = make_choropleth(choropleth_data, 'Disaster Count', color_theme)
            st.plotly_chart(fig_choropleth, use_container_width=True)
            
            st.markdown("""
            This choropleth map shows the distribution of disaster occurrences across countries. 
            Darker colors indicate a higher number of disasters in the selected time period and regions.
            """)

        # Footer
        st.markdown("---")
        st.markdown("Dashboard created with ❤️ using Streamlit")

if __name__ == "__main__":
    main()