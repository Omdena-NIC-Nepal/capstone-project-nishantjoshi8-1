import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path

# Load GeoJSON data
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "processed" / "combined_data.geojson"

st.title("Glacier Lake Mapping And Visualization")
st.write("This dashboard visualizes the  glacial lakes and associated hazards.")

# Load geospatial data
try:
    gdf = gpd.read_file(DATA_PATH)
    st.success("GeoJSON data loaded successfully.")
except Exception as e:
    st.error(f"Failed to load GeoJSON data: {e}")
    st.stop()

# Display basic information
st.subheader("Dataset Overview")
# st.write(gdf.head())
# st.write("Columns in the dataset:", gdf.columns.tolist())

# Display first few rows to get an idea of the data
st.write("First few rows of the dataset:")
st.write(gdf.head())
# Convert to WGS84 CRS if not already (for standard latitude/longitude)
gdf = gdf.to_crs(epsg=4326)

# Extract latitude and longitude from geometry
# For Point geometries, use the geometry directly
# For Polygon/MultiPolygon geometries, calculate the centroid
gdf["latitude"] = gdf.geometry.apply(lambda geom: geom.y if geom.geom_type == "Point" else geom.centroid.y)
gdf["longitude"] = gdf.geometry.apply(lambda geom: geom.x if geom.geom_type == "Point" else geom.centroid.x)

# Drop rows with missing coordinates
gdf = gdf.dropna(subset=["latitude", "longitude"])

# Optional: Show map if geometries are valid
if not gdf.empty:
    st.subheader("Map View of Glacial Lakes")
    st.map(gdf[["latitude", "longitude"]])  # Display on map
else:
    st.warning("No valid coordinates found to display on the map.")

# Select variables to analyze
st.subheader("Variable Distribution & Statistics")

numeric_cols = gdf.select_dtypes(include="number").columns.tolist()
selected_col = st.selectbox("Select a variable to analyze:", numeric_cols)

# Show summary statistics
st.write(f"Summary Statistics for `{selected_col}`")
st.write(gdf[selected_col].describe())

# Histogram
fig, ax = plt.subplots(figsize=(8, 4))
gdf[selected_col].hist(bins=30, color="steelblue", ax=ax)
ax.set_title(f"Distribution of {selected_col}")
ax.set_xlabel(selected_col)
ax.set_ylabel("Frequency")
st.pyplot(fig)

# Optional filtering by elevation, area, or other criteria
if 'elevation' in gdf.columns:
    st.subheader("Filter by Elevation")
    min_elev, max_elev = int(gdf['elevation'].min()), int(gdf['elevation'].max())
    elev_range = st.slider("Select elevation range", min_elev, max_elev, (min_elev, max_elev))
    filtered_gdf = gdf[(gdf['elevation'] >= elev_range[0]) & (gdf['elevation'] <= elev_range[1])]
    st.write(f"Filtered lakes: {len(filtered_gdf)}")
    st.map(filtered_gdf[["latitude", "longitude"]])
else:
    st.info("No 'elevation' column found for filtering.")

# You could add flood risk, area expansion, etc., if available in the dataset
