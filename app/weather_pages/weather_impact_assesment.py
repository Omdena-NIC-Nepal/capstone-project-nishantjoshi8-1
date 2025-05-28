
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from geopy.distance import geodesic
from mpl_toolkits.mplot3d import Axes3D
import os
# Load and clean dataset
# df = pd.read_csv('../feature_engineering/weather_and_temp_feature_engineering.csv')
# Get current file's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.abspath(os.path.join(BASE_DIR, '../feature_engineering/weather_and_temp_feature_engineering.csv'))

# Load data
df = pd.read_csv(DATA_PATH)
# Load dataset
df = pd.read_csv(DATA_PATH)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by='date')

st.title("🌦️ Weather Impact Assessment Dashboard")

# # Sidebar Filters
# # st.sidebar.header("Filter Options")
districts = df['district'].dropna().unique().tolist()
# selected_district = st.sidebar.selectbox("Select a District", ['All'] + districts)
selected_district = st.selectbox("Select a District", ['All'] + districts)

if selected_district != 'All':
    df = df[df['district'] == selected_district]

# 1. Precipitation Trends (Rolling Averages)
st.subheader("📉 Precipitation Rolling Patterns")
fig1, ax1 = plt.subplots()
ax1.plot(df['date'], df['precip_rolling_30d_mean'], label='30-Day Avg', color='blue')
ax1.plot(df['date'], df['precip_rolling_30d_std'], label='30-Day Std Dev', color='red', linestyle='--')
ax1.set(title='Rolling Precipitation Metrics', xlabel='Date', ylabel='Scaled Precipitation')
ax1.legend()
st.pyplot(fig1)

# 2. Drought & Heat Stress (SPI and HSI)
st.subheader("🔥 Drought & Heat Stress Trends")
fig2, ax2 = plt.subplots()
ax2.plot(df['date'], df['spi_like'], label='SPI-like (Drought Index)', color='brown')
ax2.plot(df['date'], df['heat_stress_index'], label='Heat Stress Index', color='orange')
ax2.legend()
ax2.set(title='SPI & Heat Stress Trends', xlabel='Date', ylabel='Index')
st.pyplot(fig2)

# 3. Temperature & Lag Effects
st.subheader("🌡️ Temperature & Lag Effects")
fig3, ax3 = plt.subplots()
ax3.plot(df['date'], df['temperature_avg'], label='Avg Temp', color='tomato')
ax3.plot(df['date'], df['temp_lag_1'], label='Temp Lag 1', color='purple', linestyle=':')
ax3.plot(df['date'], df['temp_lag_30'], label='Temp Lag 30', color='gray', linestyle='--')
ax3.set(title='Temperature & Lag Patterns', xlabel='Date')
ax3.legend()
st.pyplot(fig3)

# 4. Monsoon Impact
st.subheader("🌧️ Monsoon Impact")
fig4 = px.line(df, x='date', y='is_monsoon', color='district' if selected_district == 'All' else None,
               title='Monsoon Seasonality')
st.plotly_chart(fig4)

# 5. Seasonal Disaster Pattern
st.subheader("📆 Seasonal Disaster Occurrence")
if 'disaster_type' in df.columns and df['disaster_type'].notna().any():
    seasonal_df = df[df['disaster_type'].notna()]
    seasonal_df['month'] = seasonal_df['date'].dt.month
    fig5 = px.histogram(seasonal_df, x='month', color='disaster_type', barmode='group',
                        title='Disaster Frequency by Month')
    st.plotly_chart(fig5)
else:
    st.info("No disaster occurrence data available for seasonal analysis.")

# 6. Geospatial Vulnerability
st.subheader("🗺️ Spatial Risk Visualization")
ref_point = (df['latitude'].mean(), df['longitude'].mean())
df['distance_to_center_km'] = df.apply(lambda row: geodesic((row['latitude'], row['longitude']), ref_point).km, axis=1)
fig6 = px.scatter_mapbox(df, lat='latitude', lon='longitude', color='distance_to_center_km',
                         hover_data=['date'], zoom=4, mapbox_style='carto-positron',
                         title="Distance from Center (Geospatial Spread)")
st.plotly_chart(fig6)

# 7. Principal Component Impact
st.subheader("📊 PCA Components (Regional Variation)")
fig7 = px.scatter_3d(df, x='pca_1', y='pca_2', z='pca_3', color='latitude',
                     title="PCA Component Space", opacity=0.6)
st.plotly_chart(fig7)

# 8. Cluster-like Behavior via Heatmap
st.subheader("🧩 Clustering Insight via Correlation")
corr_cols = ['temperature_avg', 'precipitation', 'spi_like', 'heat_stress_index', 'precip_rolling_30d_mean']
fig8, ax8 = plt.subplots()
sns.heatmap(df[corr_cols].corr(), annot=True, cmap='coolwarm', ax=ax8)
ax8.set_title("Feature Correlation Heatmap")
st.pyplot(fig8)

# 9. Disaster-Lag Correlation
st.subheader("📈 Lag Features & Disaster Co-occurrence")
if 'disaster_type' in df.columns:
    disaster_df = df[df['disaster_type'].notna()]
    fig9 = px.scatter(disaster_df, x='temp_lag_7', y='precip_lag_7', color='disaster_type',
                      title='Lag Features at Time of Disasters')
    st.plotly_chart(fig9)

# 10. Full Table View (Toggle)
if st.checkbox("Show Full Dataset"):
    st.write(df)

