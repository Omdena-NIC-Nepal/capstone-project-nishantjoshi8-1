import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Load your dataset
df = pd.read_csv("../data/processed/dailyclimate_cleaned.csv")  # Specify the path to your raw dataset

# 1. Climate Indices
# Heat Stress Index (simple: temperature + humidity combined effect)
df['heat_stress_index'] = df['temp_2m'] + 0.1 * df['humidity_2m']

# Drought Index (simple proxy: low precipitation + high temp)
# Scale both components
precip_scaled = (df['precip'] - df['precip'].min()) / (df['precip'].max() - df['precip'].min())
temp_scaled = (df['temp_2m'] - df['temp_2m'].min()) / (df['temp_2m'].max() - df['temp_2m'].min())
df['drought_index'] = (1 - precip_scaled) + temp_scaled

# 2. Seasonal Indicators
# 1 if Monsoon (June-Sept), else 0
df['is_monsoon'] = df['month'].apply(lambda x: 1 if x in [6,7,8,9] else 0)
# 1 if Winter (Dec-Feb)
df['is_winter'] = df['month'].apply(lambda x: 1 if x in [12,1,2] else 0)

# 3. Lag Features
# Previous day's temp and precipitation (basic lagged memory)
df['temp_2m_lag1'] = df['temp_2m'].shift(1)
df['precip_lag1'] = df['precip'].shift(1)

# 4. Spatial Features
# Already have 'latitude' and 'longitude', keep them
# (Optionally, later we can calculate distance from major rivers or glaciers)

# 5. Derived Features
# Temperature Range already there ('temprange_2m')
# Wet bulb temp difference (how much wetbulb deviates from actual temp)
df['wetbulb_diff'] = df['temp_2m'] - df['wetbulbtemp_2m']

# Wind Speed Metrics: combining 10m and 50m layer info
df['avg_windspeed'] = (df['windspeed_10m'] + df['windspeed_50m']) / 2
df['max_avg_windspeed'] = (df['maxwindspeed_10m'] + df['maxwindspeed_50m']) / 2

# 6. Normalization (for modeling)
scaler = MinMaxScaler()
scaled_features = scaler.fit_transform(df[['temp_2m', 'precip', 'humidity_2m', 'windspeed_10m', 'windspeed_50m', 
                                           'earthskintemp', 'heat_stress_index', 'drought_index']])
scaled_df = pd.DataFrame(scaled_features, 
                         columns=['temp_2m_scaled', 'precip_scaled', 'humidity_2m_scaled', 
                                  'windspeed_10m_scaled', 'windspeed_50m_scaled', 
                                  'earthskintemp_scaled', 'heat_stress_index_scaled', 'drought_index_scaled'])

# Merge scaled features
df = pd.concat([df, scaled_df], axis=1)

# 7. (Optional) Dimensionality Reduction
# Not needed now because we have ~30 features — manageable.
# Later we can use PCA if needed.

# 8. Final cleanup
# Drop rows with NaN due to lag features
df = df.dropna().reset_index(drop=True)

# Save the feature-engineered dataset
df.to_csv("feature_engineered_climate_data.csv", index=False)

print("✅ Feature Engineering Complete! New dataset shape:", df.shape)
