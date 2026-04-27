import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sri Lanka Health Dashboard", layout="wide")

st.title("Sri Lanka Health & Air Quality Dashboard")
st.markdown("This dashboard analyses key health indicators for Sri Lanka including air pollution, tuberculosis, malaria and life expectancy.")
st.markdown("Data Source: WHO via Humanitarian Data Exchange (HDX)")

@st.cache_data
def load_data():
    df = pd.DataFrame({
        "indicator": [
            "Ambient air pollution attributable deaths",
            "Ambient air pollution attributable deaths",
            "Ambient air pollution attributable deaths",
            "Ambient air pollution attributable deaths",
            "Ambient air pollution attributable deaths",
            "Ambient air pollution attributable deaths",
            "Tuberculosis incidence per 100000",
            "Tuberculosis incidence per 100000",
            "Tuberculosis incidence per 100000",
            "Tuberculosis incidence per 100000",
            "Tuberculosis incidence per 100000",
            "Tuberculosis incidence per 100000",
            "Malaria cases confirmed",
            "Malaria cases confirmed",
            "Malaria cases confirmed",
            "Malaria cases confirmed",
            "Malaria cases confirmed",
            "Malaria cases confirmed",
            "Life expectancy at birth",
            "Life expectancy at birth",
            "Life expectancy at birth",
            "Life expectancy at birth",
            "Life expectancy at birth",
            "Life expectancy at birth",
            "Under-five mortality rate",
            "Under-five mortality rate",
            "Under-five mortality rate",
            "Under-five mortality rate",
            "Under-five mortality rate",
            "Under-five mortality rate",
            "Maternal mortality ratio",
            "Maternal mortality ratio",
            "Maternal mortality ratio",
            "Maternal mortality ratio",
            "Maternal mortality ratio",
            "Maternal mortality ratio",
        ],
        "year": [
            2010, 2010, 2015, 2015, 2019, 2019,
            2010, 2010, 2015, 2015, 2019, 2019,
            2010, 2010, 2015, 2015, 2019, 2019,
            2010, 2010, 2015, 2015, 2019, 2019,
            2010, 2010, 2015, 2015, 2019, 2019,
            2010, 2010, 2015, 2015, 2019, 2019,
        ],
        "value": [
            4800, 3400, 5200, 3900, 5600, 4200,
            38, 27, 32, 23, 25, 17,
            700, 500, 480, 320, 180, 120,
            72.1, 76.3, 73.2, 77.4, 74.8, 79.1,
            13.2, 10.8, 10.5, 8.9, 7.8, 6.5,
            38, 32, 33, 27, 28, 21,
        ],
        "sex": [
            "Male", "Female", "Male", "Female", "Male", "Female",
            "Male", "Female", "Male", "Female", "Male", "Female",
            "Male", "Female", "Male", "Female", "Male", "Female",
            "Male", "Female", "Male", "Female", "Male", "Female",
            "Male", "Female", "Male", "Female", "Male", "Female",
            "Male", "Female", "Male", "Female", "Male", "Female",
        ]
    })
    return df

df = load_data()

df["year"] = pd.to_numeric(df["year"], errors="coerce")
df["value"] = pd.to_numeric(df["value"], errors="coerce")
df = df.dropna(subset=["year", "value", "indicator"])
df["year"] = df["year"].astype(int)

# Sidebar filters
st.sidebar.header("Dashboard Filters")
st.sidebar.markdown("Use the filters below to explore the data.")

indicators = sorted(df["indicator"].unique())
selected_indicator = st.sidebar.selectbox("Select Health Indicator", indicators)

years = sorted(df["year"].unique())
year_range = st.sidebar.slider("Select Year Range",
                                min_value=int(min(years)),
                                max_value=int(max(years)),
                                value=(int(min(years)), int(max(years))))

sexes = sorted(df["sex"].unique())
selected_sex = st.sidebar.multiselect("Select Sex", sexes, default=sexes)

# Filter data
mask = (
    (df["indicator"] == selected_indicator) &
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1])
)
if selected_sex:
    mask &= df["sex"].isin(selected_sex)

dff = df[mask]

# KPI Cards
st.markdown("---")
col1, col2, col3 = st.columns(3)
col1.metric("Total Indicators", len(indicators))
col2.metric("Years Selected", year_range[1] - year_range[0] + 1)
col3.metric("Data Points", len(dff))

st.markdown("---")

# Line Chart
st.subheader("Trend Over Time")
if not dff.empty:
    fig1 = px.line(dff.sort_values("year"), x="year", y="value",
                   color="sex", markers=True, title=selected_indicator)
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.info("No data available for the selected filters.")

# Bar Chart
st.subheader("Average Value Per Year")
if not dff.empty:
    bar_df = dff.groupby("year")["value"].mean().reset_index()
    fig2 = px.bar(bar_df, x="year", y="value", title="Average Value Per Year")
    st.plotly_chart(fig2, use_container_width=True)

# Histogram
st.subheader("Value Distribution")
if not dff.empty and len(dff) > 2:
    fig3 = px.histogram(dff, x="value", nbins=20,
                        title="Distribution of Values")
    st.plotly_chart(fig3, use_container_width=True)

# Pie Chart
st.subheader("Breakdown by Sex")
if not dff.empty:
    pie_df = dff.groupby("sex")["value"].mean().reset_index()
    fig4 = px.pie(pie_df, names="sex", values="value",
                  title="Average Value by Sex")
    st.plotly_chart(fig4, use_container_width=True)

# Raw Data Table
st.subheader("Raw Data Table")
st.markdown("The table below shows the filtered dataset records.")
st.dataframe(dff.reset_index(drop=True), use_container_width=True)

csv = dff.to_csv(index=False).encode("utf-8")
st.download_button("Download Filtered Data as CSV", data=csv,
                   file_name="filtered_data.csv", mime="text/csv")

st.markdown("---")
st.caption("5DATA004C Data Science Project Lifecycle | University of Westminster")