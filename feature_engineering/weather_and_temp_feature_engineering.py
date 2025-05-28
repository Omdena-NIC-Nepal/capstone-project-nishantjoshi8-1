# import pandas as pd
# import numpy as np
# from sklearn.preprocessing import StandardScaler
# from sklearn.decomposition import PCA
# from geopy.distance import geodesic
# from sklearn.impute import SimpleImputer
# import os

# # === Helper Function to Load and Clean CSV ===
# def load_and_prepare_csv(filepath):
#     df = pd.read_csv(filepath)
#     df.columns = df.columns.str.strip().str.lower()
#     if 'date' in df.columns:
#         df['date'] = pd.to_datetime(df['date'], errors='coerce')
#     return df

# # === Load and Rename Columns ===
# weather_df = load_and_prepare_csv("../data/processed/weather_and_historical/processed_temp_precipitation.csv")
# weather_df.rename(columns={
#     'lat': 'latitude',
#     'lon': 'longitude',
#     't2m': 'temperature_avg',
#     'prectot': 'precipitation'
# }, inplace=True)

# extreme_df = load_and_prepare_csv("../data/processed/weather_and_historical/processed_extreme_weather_events.csv")
# extreme_df.rename(columns={'start_date': 'date'}, inplace=True)

# # === Ensure date columns are datetime ===
# weather_df['date'] = pd.to_datetime(weather_df['date'], errors='coerce')
# extreme_df['date'] = pd.to_datetime(extreme_df['date'], errors='coerce')

# # === Check required keys ===
# required_keys = ['date', 'latitude', 'longitude']
# missing_weather = [col for col in required_keys if col not in weather_df.columns]
# missing_extreme = [col for col in required_keys if col not in extreme_df.columns]

# if missing_weather or missing_extreme:
#     raise ValueError(f"Missing keys - Weather: {missing_weather}, Extreme: {missing_extreme}")

# # === Merge DataFrames ===
# df = pd.merge(weather_df, extreme_df, on=required_keys, how='outer')

# # === Sort for rolling and lag features ===
# df.sort_values(['latitude', 'longitude', 'date'], inplace=True)

# # === 1. Climate Indices ===
# df['precip_rolling_30d_mean'] = df.groupby(['latitude', 'longitude'])['precipitation'].transform(lambda x: x.rolling(30, min_periods=1).mean())
# df['precip_rolling_30d_std'] = df.groupby(['latitude', 'longitude'])['precipitation'].transform(lambda x: x.rolling(30, min_periods=1).std())
# df['spi_like'] = (df['precipitation'] - df['precip_rolling_30d_mean']) / df['precip_rolling_30d_std']

# # === 2. Heat Stress Metric ===
# if 'humidity' in df.columns:
#     df['heat_stress_index'] = df['humidity'] * df['temperature_avg']
# else:
#     df['heat_stress_index'] = df['temperature_avg']

# # === 3. Seasonal Indicators ===
# df['month'] = df['date'].dt.month
# df['is_monsoon'] = df['month'].apply(lambda x: 1 if 6 <= x <= 9 else 0)

# # === 4. Lag Features ===
# for lag in [1, 3, 7, 30]:
#     df[f'temp_lag_{lag}'] = df.groupby(['latitude', 'longitude'])['temperature_avg'].shift(lag)
#     df[f'precip_lag_{lag}'] = df.groupby(['latitude', 'longitude'])['precipitation'].shift(lag)

# # === 5. Spatial Proximity Features ===
# ref_point = (df['latitude'].mean(), df['longitude'].mean())
# df['distance_to_center_km'] = df.apply(
#     lambda row: geodesic((row['latitude'], row['longitude']), ref_point).km,
#     axis=1
# )

# # === 6. Satellite Imagery Features (Optional) ===
# if 'ndvi' in df.columns:
#     df['ndvi_trend_30d'] = df.groupby(['latitude', 'longitude'])['ndvi'].transform(lambda x: x.rolling(30, min_periods=1).mean())

# # === 7. Geographic Information ===
# df['region_id'] = df['latitude'].round(1).astype(str) + "_" + df['longitude'].round(1).astype(str)

# # === 8. Normalize and Scale Features ===
# features_to_scale = df.select_dtypes(include=[np.number]).drop(columns=['latitude', 'longitude']).columns
# # Handle NaNs before scaling
# imputer = SimpleImputer(strategy='mean')
# scaled_data = imputer.fit_transform(df[features_to_scale])
# scaler = StandardScaler()
# scaled_data = scaler.fit_transform(scaled_data)
# df[features_to_scale] = scaled_data

# # === 9. Dimensionality Reduction (PCA) ===
# pca = PCA(n_components=min(10, len(features_to_scale)))
# pca_features = pca.fit_transform(df[features_to_scale])
# pca_df = pd.DataFrame(pca_features, columns=[f'pca_{i+1}' for i in range(pca_features.shape[1])])
# df.reset_index(drop=True, inplace=True)
# df = pd.concat([df, pca_df], axis=1)

# # === 10. Save Final Output ===
# os.makedirs("../data/feature_engineering", exist_ok=True)
# df.to_csv("../data/feature_engineering/engineered_weather_data.csv", index=False)
# print("✅ Feature engineering completed and file saved.")


def run_feature_engineering():
    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    from geopy.distance import geodesic
    from sklearn.impute import SimpleImputer
    import os

    # === Helper Function to Load and Clean CSV ===
    def load_and_prepare_csv(filepath):
        df = pd.read_csv(filepath)
        df.columns = df.columns.str.strip().str.lower()
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
        return df

    # === Load and Rename Columns ===
    weather_df = load_and_prepare_csv("../data/processed/weather_and_historical/processed_temp_precipitation.csv")
    weather_df.rename(columns={
        'lat': 'latitude',
        'lon': 'longitude',
        't2m': 'temperature_avg',
        'prectot': 'precipitation'
    }, inplace=True)

    extreme_df = load_and_prepare_csv("../data/processed/weather_and_historical/processed_extreme_weather_events.csv")
    extreme_df.rename(columns={'start_date': 'date'}, inplace=True)

    # === Ensure date columns are datetime ===
    weather_df['date'] = pd.to_datetime(weather_df['date'], errors='coerce')
    extreme_df['date'] = pd.to_datetime(extreme_df['date'], errors='coerce')

    # === Check required keys ===
    required_keys = ['date', 'latitude', 'longitude']
    missing_weather = [col for col in required_keys if col not in weather_df.columns]
    missing_extreme = [col for col in required_keys if col not in extreme_df.columns]

    if missing_weather or missing_extreme:
        raise ValueError(f"Missing keys - Weather: {missing_weather}, Extreme: {missing_extreme}")

    # === Merge DataFrames ===
    df = pd.merge(weather_df, extreme_df, on=required_keys, how='outer')
    df.sort_values(['latitude', 'longitude', 'date'], inplace=True)

    # === Climate Indices ===
    df['precip_rolling_30d_mean'] = df.groupby(['latitude', 'longitude'])['precipitation'].transform(lambda x: x.rolling(30, min_periods=1).mean())
    df['precip_rolling_30d_std'] = df.groupby(['latitude', 'longitude'])['precipitation'].transform(lambda x: x.rolling(30, min_periods=1).std())
    df['spi_like'] = (df['precipitation'] - df['precip_rolling_30d_mean']) / df['precip_rolling_30d_std']

    # === Heat Stress ===
    if 'humidity' in df.columns:
        df['heat_stress_index'] = df['humidity'] * df['temperature_avg']
    else:
        df['heat_stress_index'] = df['temperature_avg']

    # === Seasonal Indicators ===
    df['month'] = df['date'].dt.month
    df['is_monsoon'] = df['month'].apply(lambda x: 1 if 6 <= x <= 9 else 0)

    # === Lag Features ===
    for lag in [1, 3, 7, 30]:
        df[f'temp_lag_{lag}'] = df.groupby(['latitude', 'longitude'])['temperature_avg'].shift(lag)
        df[f'precip_lag_{lag}'] = df.groupby(['latitude', 'longitude'])['precipitation'].shift(lag)

    # === Spatial Feature ===
    ref_point = (df['latitude'].mean(), df['longitude'].mean())
    df['distance_to_center_km'] = df.apply(lambda row: geodesic((row['latitude'], row['longitude']), ref_point).km, axis=1)

    # === NDVI Trend (Optional) ===
    if 'ndvi' in df.columns:
        df['ndvi_trend_30d'] = df.groupby(['latitude', 'longitude'])['ndvi'].transform(lambda x: x.rolling(30, min_periods=1).mean())

    # === Region ID ===
    df['region_id'] = df['latitude'].round(1).astype(str) + "_" + df['longitude'].round(1).astype(str)

    # === Scaling ===
    features_to_scale = df.select_dtypes(include=[np.number]).drop(columns=['latitude', 'longitude']).columns
    imputer = SimpleImputer(strategy='mean')
    scaled_data = imputer.fit_transform(df[features_to_scale])
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(scaled_data)
    df[features_to_scale] = scaled_data

    # === PCA ===
    pca = PCA(n_components=min(10, len(features_to_scale)))
    pca_features = pca.fit_transform(df[features_to_scale])
    pca_df = pd.DataFrame(pca_features, columns=[f'pca_{i+1}' for i in range(pca_features.shape[1])])
    df.reset_index(drop=True, inplace=True)
    df = pd.concat([df, pca_df], axis=1)

    # === Save Final Output ===
    os.makedirs("../feature_engineering", exist_ok=True)
    df.to_csv("../feature_engineering/weather_and_temp_feature_engineering.csv", index=False)
    print("✅ Feature engineering completed and file saved.")
if __name__ == "__main__":
    run_feature_engineering()
