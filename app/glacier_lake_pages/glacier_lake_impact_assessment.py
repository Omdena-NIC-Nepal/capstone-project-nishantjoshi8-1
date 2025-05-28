import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import pandas as pd
import re
import folium
from streamlit_folium import st_folium

# Load GeoJSON data
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "processed" / "combined_data.geojson"

st.title("Glacier Lake Impact Assessment")
st.write("This dashboard visualizes the potential impact of glacial lakes and associated hazards.")

# Load geospatial data
try:
    gdf = gpd.read_file(DATA_PATH)
    st.success("GeoJSON data loaded successfully.")
except Exception as e:
    st.error(f"Failed to load GeoJSON data: {e}")
    st.stop()

# Display basic information about the dataset
st.subheader("Dataset Overview")
# st.write("Columns in the dataset:", gdf.columns.tolist())

# Display first few rows to get an idea of the data
st.write("First few rows of the dataset:")
st.write(gdf.head())

# 1. Flood Risk Analysis
st.subheader("Flood Risk Analysis")
st.write("Flood risk might be higher near glaciers. We will classify flood risk based on the `dist2glac` column.")

flood_risk = gdf['dist2glac'].apply(lambda x: 'High Risk' if x < 10 else 'Low Risk')
gdf['Flood_Risk'] = flood_risk

st.write("Flood Risk Classification (based on distance to glacier):")
st.write(gdf[['gl_name', 'dist2glac', 'Flood_Risk']].head())

st.write("Flood Risk Distribution:")
sns.countplot(x='Flood_Risk', data=gdf, palette="Set2")
st.pyplot(plt)

# 2. Glacier Lake Area Expansion
st.subheader("Glacier Lake Area Expansion")

if not pd.api.types.is_datetime64_any_dtype(gdf['map60_date']):
    gdf['map60_date'] = pd.to_datetime(gdf['map60_date'], errors='coerce')

gdf = gdf.dropna(subset=['map60_date', 'area'])
area_over_time = gdf.groupby(gdf['map60_date'].dt.year)['area'].mean().reset_index()

st.write("Average Glacier Lake Area Change Over Time:")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=area_over_time, x='map60_date', y='area', marker='o', color='lightcoral')
plt.title("Average Glacier Lake Area Over Time")
plt.xlabel("Year")
plt.ylabel("Average Area (sq.km)")
plt.grid(True)
st.pyplot(fig)

area_over_time['growth_rate'] = area_over_time['area'].pct_change() * 100
st.write("Growth Rate of Glacier Lake Areas (Year-over-Year):")
st.write(area_over_time[['map60_date', 'growth_rate']].dropna())

fig_growth_rate, ax_growth_rate = plt.subplots(figsize=(10, 6))
sns.lineplot(data=area_over_time, x='map60_date', y='growth_rate', marker='o', color='green')
plt.title("Glacier Lake Area Growth Rate Over Time")
plt.xlabel("Year")
plt.ylabel("Growth Rate (%)")
plt.grid(True)
st.pyplot(fig_growth_rate)

# 3. Interactive Filtering
year_range = st.slider(
    "Select Year Range:",
    int(gdf['map60_date'].dt.year.min()), 
    int(gdf['map60_date'].dt.year.max()),
    (int(gdf['map60_date'].dt.year.min()), int(gdf['map60_date'].dt.year.max()))
)
filtered_gdf = gdf[(gdf['map60_date'].dt.year >= year_range[0]) & (gdf['map60_date'].dt.year <= year_range[1])]
st.write(f"Displaying data from {year_range[0]} to {year_range[1]}")


if 'basin' in gdf.columns:
    # selected_basin = st.selectbox("Select Basin to filter by:", options=sorted(gdf['basin'].dropna().unique()))
    basin_options = sorted(gdf['basin'].dropna().unique())
    default_basin_index = basin_options.index("Gandaki") if "Gandaki" in basin_options else 0
    selected_basin = st.selectbox("Select Basin to filter by:", options=basin_options, index=default_basin_index)

    filtered_gdf = filtered_gdf[filtered_gdf['basin'] == selected_basin]

    if 'sub_basin' in gdf.columns:
        sub_basin_options = sorted(filtered_gdf['sub_basin'].dropna().unique())
        if sub_basin_options:
            selected_sub_basin = st.selectbox("Select Sub-Basin to filter by:", options=sub_basin_options)
            filtered_gdf = filtered_gdf[filtered_gdf['sub_basin'] == selected_sub_basin]

st.write("Filtered Data (first 5 rows after filtering):")
st.write(filtered_gdf[['gl_name', 'basin', 'sub_basin', 'area', 'elevation', 'map60_date', 'latitude', 'longitude']].head())

# 4. Convert Coordinates from DMM to Decimal Degrees
def dmm_to_decimal(degree_minute_str):
    if isinstance(degree_minute_str, str):
        match = re.match(r"(\d+)[D](\d+\.\d+)[M]", degree_minute_str)
        if match:
            degrees = float(match.group(1))
            minutes = float(match.group(2))
            return degrees + (minutes / 60)
    return None

filtered_gdf['latitude'] = filtered_gdf['latitude'].apply(dmm_to_decimal)
filtered_gdf['longitude'] = filtered_gdf['longitude'].apply(dmm_to_decimal)

filtered_gdf = filtered_gdf.dropna(subset=['latitude', 'longitude'])
filtered_gdf = filtered_gdf[
    (filtered_gdf['latitude'] >= -90) & (filtered_gdf['latitude'] <= 90) &
    (filtered_gdf['longitude'] >= -180) & (filtered_gdf['longitude'] <= 180)
]

st.write(f"Remaining rows after cleaning invalid coordinates: {len(filtered_gdf)}")

if not filtered_gdf.empty:
    st.subheader("Filtered Data Map View")
    
    # Drop rows with missing or out-of-range lat/lon
    filtered_gdf = filtered_gdf.dropna(subset=['latitude', 'longitude'])
    filtered_gdf = filtered_gdf[
        (filtered_gdf['latitude'] >= -90) & (filtered_gdf['latitude'] <= 90) &
        (filtered_gdf['longitude'] >= -180) & (filtered_gdf['longitude'] <= 180)
    ]

    st.write(f"Remaining rows after cleaning invalid coordinates: {len(filtered_gdf)}")

    # Create Folium map
    avg_lat = filtered_gdf['latitude'].mean()
    avg_lon = filtered_gdf['longitude'].mean()
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=6)

    for _, row in filtered_gdf.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=row.get('gl_name', 'Unnamed Lake'),
            tooltip=row.get('Flood_Risk', 'No risk data')
        ).add_to(m)

    st_folium(m, width=800, height=500)
else:
    st.warning("No valid coordinates found in the filtered data to display on the map.")

# 6. Elevation Distribution
if 'elevation' in gdf.columns:
    st.subheader("Elevation Distribution")
    sns.histplot(gdf['elevation'], kde=True, color="skyblue", bins=30)
    plt.title("Distribution of Elevation")
    plt.xlabel("Elevation (m)")
    plt.ylabel("Frequency")
    st.pyplot(plt)
else:
    st.info("No 'elevation' column found for analysis.")
