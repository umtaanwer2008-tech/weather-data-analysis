
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Weather Analysis Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("weather_data.csv", parse_dates=["Date"])

df = load_data()

st.title("Historical Weather Data Analysis")
st.write("An interactive dashboard exploring historical weather patterns.")

# Sidebar filters
st.sidebar.header("Filters")

countries = ["All"] + sorted(df["Country/Region"].dropna().unique().tolist())
selected_country = st.sidebar.selectbox("Select Country", countries)

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

filtered_df = df.copy()

if selected_country != "All":
    filtered_df = filtered_df[
        filtered_df["Country/Region"] == selected_country
    ]

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df["Date"].dt.date >= start_date) &
        (filtered_df["Date"].dt.date <= end_date)
    ]

if filtered_df.empty:
    st.warning("No data available for these filters.")
    st.stop()

# Key metrics
st.subheader("Key Weather Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Average Temperature", round(filtered_df["temp"].mean(), 2))
col2.metric("Maximum Temperature", round(filtered_df["max"].max(), 2))
col3.metric("Average Humidity", round(filtered_df["rh"].mean(), 2))
col4.metric("Number of Days", filtered_df["Date"].nunique())

# Univariate graphs
st.subheader("Weather Distributions")

col1, col2 = st.columns(2)

with col1:
    fig = px.histogram(filtered_df, x="temp", title="Temperature Distribution")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.histogram(filtered_df, x="prcp", title="Rainfall Distribution")
    st.plotly_chart(fig, use_container_width=True)

fig = px.histogram(filtered_df, x="wdsp", title="Wind Speed Distribution")
st.plotly_chart(fig, use_container_width=True)

# Bivariate graph
st.subheader("Temperature and Humidity")

fig = px.scatter(
    filtered_df,
    x="temp",
    y="rh",
    title="Relationship Between Temperature and Humidity"
)
st.plotly_chart(fig, use_container_width=True)

# Temperature over time
st.subheader("Temperature Over Time")

daily_temp = filtered_df.groupby("Date")["temp"].mean().reset_index()

fig = px.line(
    daily_temp,
    x="Date",
    y="temp",
    title="Average Temperature Over Time"
)
st.plotly_chart(fig, use_container_width=True)

# Correlation heatmap
st.subheader("Weather Correlation Heatmap")

corr = filtered_df[["temp", "min", "max", "rh", "wdsp", "prcp"]].corr()

fig = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    title="Correlation Between Weather Variables"
)
st.plotly_chart(fig, use_container_width=True)

# Main findings
st.subheader("Main Findings")

st.write("Average temperature:", round(filtered_df["temp"].mean(), 2))
st.write("Average rainfall:", round(filtered_df["prcp"].mean(), 3))
st.write("Average wind speed:", round(filtered_df["wdsp"].mean(), 2))

# Raw data
if st.checkbox("Show Raw Weather Data"):
    st.dataframe(filtered_df)

