import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from graph-functions import load_data, data_cleaning, frequency, frequency_response

# Helper functions (load_data, initial_inspection, data_cleaning, frequency, sanitize_filename, frequency_response)
# [Include all the helper functions from the original script here]

# Enhanced plotting functions using Plotly
def plotter_disaster_frequency(frequency_dict, x_name, y_name, title):
    df = pd.DataFrame(list(frequency_dict.items()), columns=[x_name, y_name])
    fig = px.bar(df, x=x_name, y=y_name, title=title,
                 labels={x_name: x_name, y_name: y_name},
                 color=x_name, text=y_name)
    fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    return fig

def plotter_disasters_heatmap(data, index_col, columns_col, x_label, y_label, title):
    cleaned_data = data.dropna(subset=[index_col])
    cleaned_data[index_col] = cleaned_data[index_col].astype(int)
    data_cross_tab = pd.crosstab(cleaned_data[index_col], cleaned_data[columns_col])
    
    fig = px.imshow(data_cross_tab, labels=dict(x=x_label, y=y_label),
                    x=data_cross_tab.columns, y=data_cross_tab.index,
                    title=title)
    fig.update_xaxes(side="top")
    return fig

def occurrences_over_the_years(data, column_name, title):
    disaster_counts = data.groupby(column_name).size().sort_index().reset_index()
    disaster_counts.columns = [column_name, 'Count']
    
    fig = px.line(disaster_counts, x=column_name, y='Count', title=title,
                  labels={column_name: 'Year', 'Count': 'Number of Disasters'})
    fig.update_traces(mode='lines+markers')
    return fig

def plot_grouped_bar_chart(yes, no, title='Comparative Regional Response Rates'):
    regions = list(yes.keys())
    yes_counts = [yes.get(region, 0) for region in regions]
    no_counts = [no.get(region, 0) for region in regions]
    
    fig = go.Figure(data=[
        go.Bar(name='Yes Responses', x=regions, y=yes_counts, text=yes_counts),
        go.Bar(name='No Responses', x=regions, y=no_counts, text=no_counts)
    ])
    
    fig.update_layout(barmode='group', title=title,
                      xaxis_title='Region', yaxis_title='Frequency')
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    return fig

# New function: Animated time series of disasters
def animate_disasters_over_time(data):
    data['Year'] = pd.to_datetime(data['Start Year'], format='%Y')
    disaster_counts = data.groupby(['Year', 'Disaster Subgroup']).size().reset_index(name='Count')
    
    fig = px.scatter(disaster_counts, x="Year", y="Count", size="Count", color="Disaster Subgroup",
                     hover_name="Disaster Subgroup", log_y=True, size_max=60,
                     range_y=[1,disaster_counts['Count'].max()],
                     title="Disaster Occurrences Over Time")
    
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="date"))
    return fig

# Main Streamlit App
def main():
    st.title("Enhanced Disaster Analysis Dashboard")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        data = load_data(uploaded_file, sep=';', encoding='latin-1', header=0)
        data_clean = data_cleaning(data, 10)

        st.sidebar.header("Choose Visualization")
        viz_option = st.sidebar.selectbox(
            "Select a visualization",
            ("Disaster Subgroup Frequency", "Disaster Type Distribution", "Monthly Distribution",
             "Trend Over Years", "Heatmap by Type and Month", "Annual Heatmap",
             "Regional Response Frequency", "Comparative Regional Response",
             "Animated Time Series")
        )

        if viz_option == "Disaster Subgroup Frequency":
            freq_dict = frequency(data_clean, 'Disaster Subgroup')
            fig = plotter_disaster_frequency(freq_dict, 'Disaster Types Subgroup', 'Frequency', 'Interactive Bar Chart of Disaster Subgroup Occurrences')
            st.plotly_chart(fig)

        elif viz_option == "Disaster Type Distribution":
            freq_dict = frequency(data_clean, 'Disaster Type')
            fig = plotter_disaster_frequency(freq_dict, 'Disaster Types', 'Frequency', 'Interactive Bar Chart of Disaster Types Distribution')
            st.plotly_chart(fig)

        elif viz_option == "Monthly Distribution":
            freq_dict = frequency(data_clean, 'Start Month')
            fig = plotter_disaster_frequency(freq_dict, 'Months', 'Number of Disasters', 'Interactive Monthly Distribution of Disasters')
            st.plotly_chart(fig)

        elif viz_option == "Trend Over Years":
            fig = occurrences_over_the_years(data_clean, 'Start Year', 'Interactive Trend of Disaster Incidences Over the Years')
            st.plotly_chart(fig)

        elif viz_option == "Heatmap by Type and Month":
            fig = plotter_disasters_heatmap(data_clean, 'Start Month', 'Disaster Subgroup', 'Disaster Type', 'Month', 'Interactive Heatmap of Disaster Occurrences by Type and Month')
            st.plotly_chart(fig)

        elif viz_option == "Annual Heatmap":
            fig = plotter_disasters_heatmap(data_clean, 'Start Year', 'Disaster Subgroup', 'Disaster Type', 'Years', 'Interactive Heatmap of Annual Disaster Frequency by Type')
            st.plotly_chart(fig)

        elif viz_option == "Regional Response Frequency":
            freq_dict = frequency(data_clean, 'Region')
            fig = plotter_disaster_frequency(freq_dict, 'Regions', 'Responses', 'Interactive Regional Disaster Response Frequency OFDA/BHA')
            st.plotly_chart(fig)

        elif viz_option == "Comparative Regional Response":
            yes_dict = frequency_response(data_clean, 'Yes', 'Region')
            no_dict = frequency_response(data_clean, 'No', 'Region')
            fig = plot_grouped_bar_chart(yes_dict, no_dict)
            st.plotly_chart(fig)

        elif viz_option == "Animated Time Series":
            fig = animate_disasters_over_time(data_clean)
            st.plotly_chart(fig)

if __name__ == "__main__":
    main()