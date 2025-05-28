
# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import plotly.express as px
# from matplotlib.animation import FuncAnimation

# # Load data
# df = pd.read_csv('./../../feature_engineering/weather_and_temp_feature_engineering.csv')
# df['date'] = pd.to_datetime(df['date'])
# df = df.sort_values('date')

# st.title("📊 Weather Data Visualization Dashboard")

# # Sidebar Filter
# districts = df['district'].dropna().unique().tolist()
# selected_district = st.sidebar.selectbox("Select District", ['All'] + districts)
# if selected_district != 'All':
#     df = df[df['district'] == selected_district]

# # 1. Time-Series Plot
# st.subheader("📈 Temperature and Precipitation Over Time")
# fig1, ax1 = plt.subplots()
# ax1.plot(df['date'], df['temperature_avg'], label='Temperature', color='red')
# ax1.set_ylabel('Temperature (°C)', color='red')
# ax2 = ax1.twinx()
# ax2.plot(df['date'], df['precipitation'], label='Precipitation', color='blue')
# ax2.set_ylabel('Precipitation (mm)', color='blue')
# ax1.set_title('Temperature and Precipitation Time Series')
# st.pyplot(fig1)

# # 2. Heatmap of Weather Metrics
# st.subheader("🌡️ Heatmap of Average Weather Metrics Across Districts")
# heat_df = df.groupby('district')[['temperature_avg', 'precipitation', 'spi_like', 'heat_stress_index']].mean()
# fig2, ax2 = plt.subplots(figsize=(10, 6))
# sns.heatmap(heat_df, annot=True, cmap='coolwarm', ax=ax2)
# ax2.set_title("Heatmap of Climate Metrics by District")
# st.pyplot(fig2)

# # 3. Geospatial Map with Weather Anomalies
# st.subheader("🗺️ Geospatial Weather Anomalies Map")
# fig3 = px.scatter_mapbox(df, lat="latitude", lon="longitude", color="spi_like",
#                          hover_data=["temperature_avg", "precipitation"],
#                          mapbox_style="open-street-map", zoom=4, title="SPI-like (Drought) Anomalies Map")
# st.plotly_chart(fig3)

# # 4. Animated Change Over Time
# st.subheader("🎞️ Animated Monthly Weather Changes")
# df['month_year'] = df['date'].dt.to_period('M').astype(str)
# monthly_avg = df.groupby(['month_year', 'district'])[['temperature_avg', 'precipitation']].mean().reset_index()
# fig4 = px.line(monthly_avg, x='month_year', y='temperature_avg', color='district',
#                title="Animated Monthly Average Temperature", animation_frame='month_year')
# st.plotly_chart(fig4)

# # 5. Bar Graph of Disaster Frequency
# st.subheader("📊 Disaster Frequencies by Type")
# if 'disaster_type' in df.columns:
#     disaster_counts = df['disaster_type'].value_counts().reset_index()
#     disaster_counts.columns = ['Disaster Type', 'Count']
#     fig5 = px.bar(disaster_counts, x='Disaster Type', y='Count', color='Disaster Type',
#                   title="Disaster Frequency by Type")
#     st.plotly_chart(fig5)

# # 6. Boxplot of Monthly SPI/HSI
# st.subheader("📦 Monthly Distribution of SPI and HSI")
# df['month'] = df['date'].dt.month
# fig6, ax6 = plt.subplots(figsize=(12, 5))
# sns.boxplot(x='month', y='spi_like', data=df, ax=ax6)
# ax6.set_title('Monthly Distribution of SPI-like (Drought Index)')
# st.pyplot(fig6)

# fig7, ax7 = plt.subplots(figsize=(12, 5))
# sns.boxplot(x='month', y='heat_stress_index', data=df, ax=ax7)
# ax7.set_title('Monthly Distribution of Heat Stress Index')
# st.pyplot(fig7)

# # 7. Scatter Plot for Lag Relationship
# st.subheader("🔁 Lag Relationship: Precipitation vs Disaster Occurrence")
# if 'disaster_type' in df.columns:
#     fig8 = px.scatter(df[df['disaster_type'].notna()], x='precip_lag_7', y='temp_lag_7',
#                       color='disaster_type', title='Precipitation Lag 7 vs Temperature Lag 7 at Disaster Times')
#     st.plotly_chart(fig8)

# # 8. Line Chart for Rolling Means
# st.subheader("📉 Rolling Mean and Std of Precipitation")
# fig9, ax9 = plt.subplots()
# ax9.plot(df['date'], df['precip_rolling_30d_mean'], label='30d Mean', color='blue')
# ax9.plot(df['date'], df['precip_rolling_30d_std'], label='30d Std Dev', color='gray', linestyle='--')
# ax9.legend()
# ax9.set_title("Rolling 30-Day Precipitation Stats")
# st.pyplot(fig9)

# # 9. PCA Biplots
# st.subheader("🧬 PCA Components Scatter")
# fig10 = px.scatter_3d(df, x='pca_1', y='pca_2', z='pca_3', color='temperature_avg',
#                       title="PCA Component Scatter Colored by Temperature")
# st.plotly_chart(fig10)

# # 10. Correlation Matrix
# st.subheader("🔗 Climate Feature Correlation Matrix")
# features = ['temperature_avg', 'precipitation', 'spi_like', 'heat_stress_index',
#             'precip_rolling_30d_mean', 'precip_rolling_30d_std']
# fig11, ax11 = plt.subplots()
# sns.heatmap(df[features].corr(), annot=True, cmap='coolwarm', ax=ax11)
# ax11.set_title("Correlation Matrix of Climate Features")
# st.pyplot(fig11)

# # Show full data
# if st.checkbox("Show Full Data Table"):
#     st.write(df)


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

# Resolve the correct absolute path to the CSV file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.abspath(os.path.join(BASE_DIR, '../feature_engineering/weather_and_temp_feature_engineering.csv'))

# Load data
df = pd.read_csv(DATA_PATH)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

st.title("📊 Weather Data Visualization Dashboard")

# Sidebar Filter
# districts = df['district'].dropna().unique().tolist()
# selected_district = st.sidebar.selectbox("Select District", ['All'] + districts)
# if selected_district != 'All':
#     df = df[df['district'] == selected_district]

# 1. Time-Series Plot
st.subheader("📈 Temperature and Precipitation Over Time")
fig1, ax1 = plt.subplots()
ax1.plot(df['date'], df['temperature_avg'], label='Temperature', color='red')
ax1.set_ylabel('Temperature (°C)', color='red')
ax2 = ax1.twinx()
ax2.plot(df['date'], df['precipitation'], label='Precipitation', color='blue')
ax2.set_ylabel('Precipitation (mm)', color='blue')
ax1.set_title('Temperature and Precipitation Time Series')
st.pyplot(fig1)

# 2. Heatmap of Weather Metrics
st.subheader("🌡️ Heatmap of Average Weather Metrics Across Districts")
heat_df = df.groupby('district')[['temperature_avg', 'precipitation', 'spi_like', 'heat_stress_index']].mean()
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.heatmap(heat_df, annot=True, cmap='coolwarm', ax=ax2)
ax2.set_title("Heatmap of Climate Metrics by District")
st.pyplot(fig2)

# 3. Geospatial Map with Weather Anomalies
st.subheader("🗺️ Geospatial Weather Anomalies Map")
fig3 = px.scatter_mapbox(df, lat="latitude", lon="longitude", color="spi_like",
                         hover_data=["temperature_avg", "precipitation"],
                         mapbox_style="open-street-map", zoom=4, title="SPI-like (Drought) Anomalies Map")
st.plotly_chart(fig3)

# # 4. Animated Change Over Time
# st.subheader("🎞️ Animated Monthly Weather Changes")
# df['month_year'] = df['date'].dt.to_period('M').astype(str)
# monthly_avg = df.groupby(['month_year', 'district'])[['temperature_avg', 'precipitation']].mean().reset_index()
# fig4 = px.line(monthly_avg, x='month_year', y='temperature_avg', color='district',
#                title="Animated Monthly Average Temperature", animation_frame='month_year')
# st.plotly_chart(fig4)

# 5. Bar Graph of Disaster Frequency
st.subheader("📊 Disaster Frequencies by Type")
if 'disaster_type' in df.columns:
    disaster_counts = df['disaster_type'].value_counts().reset_index()
    disaster_counts.columns = ['Disaster Type', 'Count']
    fig5 = px.bar(disaster_counts, x='Disaster Type', y='Count', color='Disaster Type',
                  title="Disaster Frequency by Type")
    st.plotly_chart(fig5)

# 6. Boxplot of Monthly SPI/HSI
st.subheader("📦 Monthly Distribution of SPI and HSI")
df['month'] = df['date'].dt.month
fig6, ax6 = plt.subplots(figsize=(12, 5))
sns.boxplot(x='month', y='spi_like', data=df, ax=ax6)
ax6.set_title('Monthly Distribution of SPI-like (Drought Index)')
st.pyplot(fig6)

fig7, ax7 = plt.subplots(figsize=(12, 5))
sns.boxplot(x='month', y='heat_stress_index', data=df, ax=ax7)
ax7.set_title('Monthly Distribution of Heat Stress Index')
st.pyplot(fig7)

# 7. Scatter Plot for Lag Relationship
st.subheader("🔁 Lag Relationship: Precipitation vs Disaster Occurrence")
if 'disaster_type' in df.columns:
    fig8 = px.scatter(df[df['disaster_type'].notna()], x='precip_lag_7', y='temp_lag_7',
                      color='disaster_type', title='Precipitation Lag 7 vs Temperature Lag 7 at Disaster Times')
    st.plotly_chart(fig8)

# 8. Line Chart for Rolling Means
st.subheader("📉 Rolling Mean and Std of Precipitation")
fig9, ax9 = plt.subplots()
ax9.plot(df['date'], df['precip_rolling_30d_mean'], label='30d Mean', color='blue')
ax9.plot(df['date'], df['precip_rolling_30d_std'], label='30d Std Dev', color='gray', linestyle='--')
ax9.legend()
ax9.set_title("Rolling 30-Day Precipitation Stats")
st.pyplot(fig9)

# 9. PCA Biplots
st.subheader("🧬 PCA Components Scatter")
if all(col in df.columns for col in ['pca_1', 'pca_2', 'pca_3']):
    fig10 = px.scatter_3d(df, x='pca_1', y='pca_2', z='pca_3', color='temperature_avg',
                          title="PCA Component Scatter Colored by Temperature")
    st.plotly_chart(fig10)
else:
    st.warning("PCA columns not found in the dataset.")

# 10. Correlation Matrix
st.subheader("🔗 Climate Feature Correlation Matrix")
features = ['temperature_avg', 'precipitation', 'spi_like', 'heat_stress_index',
            'precip_rolling_30d_mean', 'precip_rolling_30d_std']
available_features = [f for f in features if f in df.columns]
if available_features:
    fig11, ax11 = plt.subplots()
    sns.heatmap(df[available_features].corr(), annot=True, cmap='coolwarm', ax=ax11)
    ax11.set_title("Correlation Matrix of Climate Features")
    st.pyplot(fig11)
else:
    st.warning("Correlation features not found in the dataset.")

# Show full data
if st.checkbox("Show Full Data Table"):
    st.write(df)
