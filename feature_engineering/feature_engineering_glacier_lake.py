# ### Feature Engineering for combined_data.geojson

# import pandas as pd
# import geopandas as gpd
# import numpy as np
# import os
# from sklearn.preprocessing import StandardScaler, LabelEncoder

# # Load the dataset
# gdf = gpd.read_file('../data/processed/combined_data.geojson')

# # 1. Handle Missing Values
# print("\n--- Handling Missing Values ---")
# # For numerical columns: fill with median
# numerical_cols = gdf.select_dtypes(include=[np.number]).columns
# for col in numerical_cols:
#     median_val = gdf[col].median()
#     gdf[col].fillna(median_val, inplace=True)

# # For categorical columns: fill with mode
# categorical_cols = gdf.select_dtypes(include=['object']).columns
# for col in categorical_cols:
#     mode_val = gdf[col].mode()[0]
#     gdf[col].fillna(mode_val, inplace=True)

# # 2. Feature Creation
# print("\n--- Creating New Features ---")
# # Example: If temperature and precipitation exist, create a temp/precip ratio
# if set(['temperature', 'precipitation']).issubset(gdf.columns):
#     gdf['temp_precip_ratio'] = gdf['temperature'] / (gdf['precipitation'] + 1e-5)

# # Example: Create a normalized elevation feature if 'elevation' exists
# if 'elevation' in gdf.columns:
#     gdf['elevation_norm'] = (gdf['elevation'] - gdf['elevation'].min()) / (gdf['elevation'].max() - gdf['elevation'].min())

# # 3. Encoding Categorical Variables
# print("\n--- Encoding Categorical Variables ---")
# le = LabelEncoder()
# for col in categorical_cols:
#     if gdf[col].nunique() < 50:  # Only encode if unique values are manageable
#         gdf[col] = le.fit_transform(gdf[col])

# # 4. Scaling Numerical Features
# print("\n--- Scaling Numerical Features ---")
# scaler = StandardScaler()
# gdf_scaled = gdf.copy()
# gdf_scaled[numerical_cols] = scaler.fit_transform(gdf_scaled[numerical_cols])

# # 5. Save Engineered Data
# print("\n--- Saving the Engineered Dataset ---")
# output_path = './feature_engineering_glacier_lake_data.geojson'
# os.makedirs(os.path.dirname(output_path), exist_ok=True)

# gdf_scaled.to_file(output_path, driver='GeoJSON')

# print(f"Feature engineered data saved at {output_path}")

# ### Done!


# import pandas as pd
# import geopandas as gpd
# import numpy as np
# import os
# from sklearn.preprocessing import StandardScaler, OrdinalEncoder

# # Load the dataset
# gdf = gpd.read_file('../data/processed/combined_data.geojson')

# # 1. Handle Missing Values - Bulk Method
# print("\n--- Handling Missing Values ---")
# numerical_cols = gdf.select_dtypes(include=[np.number]).columns
# categorical_cols = gdf.select_dtypes(include=['object']).columns

# # Numerical: Fill all at once
# gdf[numerical_cols] = gdf[numerical_cols].fillna(gdf[numerical_cols].median())

# # Categorical: Fill all at once
# gdf[categorical_cols] = gdf[categorical_cols].fillna(gdf[categorical_cols].mode().iloc[0])

# # 2. Feature Creation
# print("\n--- Creating New Features ---")
# if set(['temperature', 'precipitation']).issubset(gdf.columns):
#     gdf['temp_precip_ratio'] = gdf['temperature'] / (gdf['precipitation'] + 1e-5)

# if 'elevation' in gdf.columns:
#     gdf['elevation_norm'] = (gdf['elevation'] - gdf['elevation'].min()) / (gdf['elevation'].max() - gdf['elevation'].min())

# # 3. Encoding Categorical Variables - Fast Encoding
# print("\n--- Encoding Categorical Variables ---")
# low_cardinality_cols = [col for col in categorical_cols if gdf[col].nunique() < 50]

# encoder = OrdinalEncoder()
# gdf[low_cardinality_cols] = encoder.fit_transform(gdf[low_cardinality_cols])

# # 4. Scaling Numerical Features
# print("\n--- Scaling Numerical Features ---")
# scaler = StandardScaler()
# gdf[numerical_cols] = scaler.fit_transform(gdf[numerical_cols])

# # 5. Save Engineered Data
# print("\n--- Saving the Engineered Dataset ---")
# output_path = './feature_engineering_glacier_lake_data.geojson'
# os.makedirs(os.path.dirname(output_path), exist_ok=True)

# gdf.to_file(output_path, driver='GeoJSON')

# print(f"Feature engineered data saved at {output_path}")




# import pandas as pd
# import geopandas as gpd
# import numpy as np
# import os
# from sklearn.preprocessing import StandardScaler, OrdinalEncoder

# # 1. Load the dataset
# print("\n📥 Loading dataset...")
# gdf = gpd.read_file('../data/processed/combined_data.geojson')

# # 2. Handle Missing Values
# print("\n🛠 Handling Missing Values...")
# numerical_cols = gdf.select_dtypes(include=[np.number]).columns.tolist()
# categorical_cols = gdf.select_dtypes(include=['object']).columns.tolist()

# # Numerical: Fill all at once with median
# gdf[numerical_cols] = gdf[numerical_cols].fillna(gdf[numerical_cols].median())

# # Categorical: Fill all at once with mode
# gdf[categorical_cols] = gdf[categorical_cols].fillna(gdf[categorical_cols].mode().iloc[0])

# # 3. Feature Creation
# print("\n✨ Creating New Features...")

# # Temperature-Precipitation Ratio
# if set(['temperature', 'precipitation']).issubset(gdf.columns):
#     gdf['temp_precip_ratio'] = gdf['temperature'] / (gdf['precipitation'] + 1e-5)

# # Normalized Elevation
# if 'elevation' in gdf.columns:
#     gdf['elevation_norm'] = (gdf['elevation'] - gdf['elevation'].min()) / (gdf['elevation'].max() - gdf['elevation'].min())

# # 4. 🎯 Create Synthetic Impact Score
# print("\n🎯 Generating Synthetic Impact Score...")

# # Ensure essential fields exist, otherwise fill dummy small values
# essential_fields = ['lake_area', 'distance_to_glacier', 'precipitation', 'temperature']
# for col in essential_fields:
#     if col not in gdf.columns:
#         gdf[col] = np.random.uniform(0.1, 1.0, len(gdf))  # Tiny random fallback

# # Calculate Impact Score
# gdf['impact_score'] = (
#     0.4 * gdf['lake_area'].fillna(0) +
#     0.3 * (1 / (gdf['distance_to_glacier'].fillna(1))) +
#     0.2 * gdf['precipitation'].fillna(0) +
#     0.1 * gdf['temperature'].fillna(0)
# )

# # Normalize Impact Score (0–100)
# gdf['impact_score'] = 100 * (gdf['impact_score'] - gdf['impact_score'].min()) / (gdf['impact_score'].max() - gdf['impact_score'].min())

# # 5. Encoding Categorical Variables
# print("\n🔢 Encoding Categorical Variables...")
# low_cardinality_cols = [col for col in categorical_cols if gdf[col].nunique() < 50]

# encoder = OrdinalEncoder()
# gdf[low_cardinality_cols] = encoder.fit_transform(gdf[low_cardinality_cols])

# # 6. Scaling Numerical Features
# print("\n📈 Scaling Numerical Features...")
# scaler = StandardScaler()
# gdf[numerical_cols] = scaler.fit_transform(gdf[numerical_cols])

# # 7. Save the Engineered Data
# print("\n💾 Saving the Engineered Dataset...")
# output_path = '../feature_engineering/feature_engineering_glacier_lake_data.geojson'
# os.makedirs(os.path.dirname(output_path), exist_ok=True)

# gdf.to_file(output_path, driver='GeoJSON')

# print(f"\n✅ Feature engineered data with 'impact_score' saved at {output_path}")


# import pandas as pd
# import geopandas as gpd
# import numpy as np
# import os
# from sklearn.preprocessing import StandardScaler, OrdinalEncoder

# # 1. Load the dataset
# print("\n📥 Loading dataset...")
# gdf = gpd.read_file('../data/processed/combined_data.geojson')

# # 2. Handle Missing Values
# print("\n🛠 Handling Missing Values...")
# numerical_cols = gdf.select_dtypes(include=[np.number]).columns.tolist()
# categorical_cols = gdf.select_dtypes(include=['object']).columns.tolist()

# # Numerical: Fill all at once with median
# gdf[numerical_cols] = gdf[numerical_cols].fillna(gdf[numerical_cols].median())

# # Categorical: Fill all at once with mode
# gdf[categorical_cols] = gdf[categorical_cols].fillna(gdf[categorical_cols].mode().iloc[0])

# # 3. Feature Creation
# print("\n✨ Creating New Features...")

# # Temperature-Precipitation Ratio
# if set(['temperature', 'precipitation']).issubset(gdf.columns):
#     gdf['temp_precip_ratio'] = gdf['temperature'] / (gdf['precipitation'] + 1e-5)

# # Normalized Elevation
# if 'elevation' in gdf.columns:
#     gdf['elevation_norm'] = (gdf['elevation'] - gdf['elevation'].min()) / (gdf['elevation'].max() - gdf['elevation'].min())

# # 4. 🎯 Create Synthetic Impact Score
# print("\n🎯 Generating Synthetic Impact Score...")

# # Ensure essential fields exist, otherwise fill dummy small values
# essential_fields = ['lake_area', 'distance_to_glacier', 'precipitation', 'temperature']
# for col in essential_fields:
#     if col not in gdf.columns:
#         gdf[col] = np.random.uniform(0.1, 1.0, len(gdf))  # Tiny random fallback

# # Calculate Impact Score
# gdf['impact_score'] = (
#     0.4 * gdf['lake_area'].fillna(0) +
#     0.3 * (1 / (gdf['distance_to_glacier'].fillna(1))) +
#     0.2 * gdf['precipitation'].fillna(0) +
#     0.1 * gdf['temperature'].fillna(0)
# )

# # Normalize Impact Score (0–100)
# gdf['impact_score'] = 100 * (gdf['impact_score'] - gdf['impact_score'].min()) / (gdf['impact_score'].max() - gdf['impact_score'].min())

# # 5. Create Classification Target Columns

# # --- Climate Zone (Categorical) ---
# # Simple example based on temperature (You can adjust thresholds based on your needs)
# gdf['climate_zone'] = pd.cut(gdf['temperature'], bins=[-np.inf, 0, 10, 20, 30, np.inf], labels=['Polar', 'Cold', 'Temperate', 'Hot', 'Tropical'])

# # --- Extreme Event (Binary) ---
# # Example: High precipitation could be indicative of extreme events (e.g., floods)
# gdf['extreme_event'] = (gdf['precipitation'] > gdf['precipitation'].median()).astype(int)

# # --- Vulnerability Level (Ordinal) ---
# # Example: Higher impact score could mean higher vulnerability
# gdf['vulnerability_level'] = pd.cut(gdf['impact_score'], bins=[-np.inf, 25, 50, 75, 100], labels=['Low', 'Medium', 'High', 'Very High'])

# # 6. Encoding Categorical Variables
# print("\n🔢 Encoding Categorical Variables...")
# low_cardinality_cols = [col for col in categorical_cols if gdf[col].nunique() < 50]

# encoder = OrdinalEncoder()
# gdf[low_cardinality_cols] = encoder.fit_transform(gdf[low_cardinality_cols])

# # 7. Scaling Numerical Features
# print("\n📈 Scaling Numerical Features...")
# scaler = StandardScaler()
# gdf[numerical_cols] = scaler.fit_transform(gdf[numerical_cols])

# # 8. Save the Engineered Data
# print("\n💾 Saving the Engineered Dataset...")
# output_path = '../feature_engineering/feature_engineering_glacier_lake_data.geojson'
# os.makedirs(os.path.dirname(output_path), exist_ok=True)

# gdf.to_file(output_path, driver='GeoJSON')

# print(f"\n✅ Feature engineered data with 'impact_score' saved at {output_path}")


# import pandas as pd
# import geopandas as gpd
# import numpy as np
# import os
# from sklearn.preprocessing import StandardScaler, OrdinalEncoder

# # 1. Load the dataset
# print("\n📥 Loading dataset...")
# gdf = gpd.read_file('../data/processed/combined_data.geojson')

# # 2. Handle Missing Values
# print("\n🛠 Handling Missing Values...")

# # Select only numeric columns
# numerical_cols = gdf.select_dtypes(include=[np.number]).columns.tolist()

# # Fill missing values for numeric columns with the median
# gdf[numerical_cols] = gdf[numerical_cols].fillna(gdf[numerical_cols].median())

# # 3. Feature Creation
# print("\n✨ Creating New Features...")

# # Temperature-Precipitation Ratio
# if set(['temperature', 'precipitation']).issubset(gdf.columns):
#     gdf['temp_precip_ratio'] = gdf['temperature'] / (gdf['precipitation'] + 1e-5)

# # Normalized Elevation
# if 'elevation' in gdf.columns:
#     gdf['elevation_norm'] = (gdf['elevation'] - gdf['elevation'].min()) / (gdf['elevation'].max() - gdf['elevation'].min())

# # 4. 🎯 Create Synthetic Impact Score
# print("\n🎯 Generating Synthetic Impact Score...")

# # Ensure essential fields exist, otherwise fill dummy small values
# essential_fields = ['lake_area', 'distance_to_glacier', 'precipitation', 'temperature']
# for col in essential_fields:
#     if col not in gdf.columns:
#         gdf[col] = np.random.uniform(0.1, 1.0, len(gdf))  # Tiny random fallback

# # Calculate Impact Score
# gdf['impact_score'] = (
#     0.4 * gdf['lake_area'].fillna(0) +
#     0.3 * (1 / (gdf['distance_to_glacier'].fillna(1))) +
#     0.2 * gdf['precipitation'].fillna(0) +
#     0.1 * gdf['temperature'].fillna(0)
# )

# # Normalize Impact Score (0–100)
# gdf['impact_score'] = 100 * (gdf['impact_score'] - gdf['impact_score'].min()) / (gdf['impact_score'].max() - gdf['impact_score'].min())

# # 5. Create Classification Target Columns (skip for numeric-only)

# # 6. Encoding Categorical Variables (skip since only numeric features are needed)

# # 7. Scaling Numerical Features
# print("\n📈 Scaling Numerical Features...")

# # Remove non-numeric columns to ensure only numerical columns are used
# gdf_numeric = gdf[numerical_cols + ['impact_score']]  # Include 'impact_score' in the numeric columns

# # Ensure 'impact_score' is used as a target and other features are numeric
# X = gdf_numeric.drop(columns=['impact_score'], errors='ignore')  # Features
# y = gdf_numeric['impact_score']  # Target

# # Ensure no row count mismatch
# print(f"X shape: {X.shape}, y shape: {y.shape}")

# # 8. Scaling
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(X)

# # 9. Save the Engineered Data (Numeric-only)
# print("\n💾 Saving the Engineered Dataset...")

# # Create a new GeoDataFrame with the scaled data and the geometry
# gdf_numeric_scaled = pd.DataFrame(X_scaled, columns=X.columns)
# gdf_numeric_scaled['impact_score'] = y  # Add target column back for saving

# # Add the original geometry column back to the DataFrame
# gdf_numeric_scaled['geometry'] = gdf['geometry']  # Ensure 'geometry' column is retained

# # Convert back to GeoDataFrame
# gdf_numeric_scaled = gpd.GeoDataFrame(gdf_numeric_scaled, geometry='geometry')

# # Save it as GeoJSON
# output_path = '../feature_engineering/feature_engineering_glacier_lake_data_numeric_only.geojson'
# os.makedirs(os.path.dirname(output_path), exist_ok=True)

# gdf_numeric_scaled.to_file(output_path, driver='GeoJSON')

# print(f"\n✅ Feature engineered data with numeric-only values and 'impact_score' saved at {output_path}")


import pandas as pd
import geopandas as gpd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler

# 1. Load the dataset
print("\n📥 Loading dataset...")
gdf = gpd.read_file('../data/processed/combined_data.geojson')
print(gdf.columns)

# 2. Handle Missing Values
print("\n🛠 Handling Missing Values...")

# Select only numeric columns
numerical_cols = gdf.select_dtypes(include=[np.number]).columns.tolist()

# Fill missing values for numeric columns with the median
gdf[numerical_cols] = gdf[numerical_cols].fillna(gdf[numerical_cols].median())

# 3. Feature Creation
print("\n✨ Creating New Features...")

# Temperature-Precipitation Ratio
if set(['temperature', 'precipitation']).issubset(gdf.columns):
    gdf['temp_precip_ratio'] = gdf['temperature'] / (gdf['precipitation'] + 1e-5)

# Normalized Elevation
if 'elevation' in gdf.columns:
    gdf['elevation_norm'] = (gdf['elevation'] - gdf['elevation'].min()) / (gdf['elevation'].max() - gdf['elevation'].min())

# 4. 🎯 Create Synthetic Impact Score
print("\n🎯 Generating Synthetic Impact Score...")

# Ensure essential fields exist, otherwise fill dummy small values
essential_fields = ['lake_area', 'distance_to_glacier', 'precipitation', 'temperature']
for col in essential_fields:
    if col not in gdf.columns:
        gdf[col] = np.random.uniform(0.1, 1.0, len(gdf))  # Tiny random fallback

# Calculate Impact Score
gdf['impact_score'] = (
    0.4 * gdf['lake_area'].fillna(0) +
    0.3 * (1 / (gdf['distance_to_glacier'].fillna(1))) +
    0.2 * gdf['precipitation'].fillna(0) +
    0.1 * gdf['temperature'].fillna(0)
)

# Normalize Impact Score (0–100)
gdf['impact_score'] = 100 * (gdf['impact_score'] - gdf['impact_score'].min()) / (gdf['impact_score'].max() - gdf['impact_score'].min())

# 5. Create Classification Target Columns

# --- Calculate Climate Zone ---
def calculate_climate_zone(row):
    if row['temperature'] > 25 and row['precipitation'] > 1000:
        return 'Tropical'
    elif row['temperature'] > 15 and row['precipitation'] > 500:
        return 'Temperate'
    else:
        return 'Arid'

gdf['climate_zone'] = gdf.apply(calculate_climate_zone, axis=1)

# --- Calculate Extreme Event ---
def calculate_extreme_event(row):
    if row['precipitation'] > 1500 or row['temperature'] > 35:
        return 1  # Extreme event
    return 0  # Not an extreme event

gdf['extreme_event'] = gdf.apply(calculate_extreme_event, axis=1)

# --- Calculate Vulnerability Level ---
def calculate_vulnerability_level(row):
    if row['lake_area'] > 1000 and row['distance_to_glacier'] < 50:
        return 'High'
    elif row['lake_area'] > 500 and row['distance_to_glacier'] < 100:
        return 'Medium'
    else:
        return 'Low'

gdf['vulnerability_level'] = gdf.apply(calculate_vulnerability_level, axis=1)

# 6. Encoding Categorical Variables (skip since only numeric features are needed)

# 7. Scaling Numerical Features
print("\n📈 Scaling Numerical Features...")

# Remove non-numeric columns to ensure only numerical columns are used
gdf_numeric = gdf[numerical_cols + ['impact_score']]  # Include 'impact_score' in the numeric columns

# Ensure 'impact_score' is used as a target and other features are numeric
X = gdf_numeric.drop(columns=['impact_score'], errors='ignore')  # Features
y = gdf_numeric['impact_score']  # Target

# Ensure no row count mismatch
print(f"X shape: {X.shape}, y shape: {y.shape}")

# 8. Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 9. Save the Engineered Data (Numeric-only)
print("\n💾 Saving the Engineered Dataset...")

# Create a new GeoDataFrame with the scaled data and the geometry
gdf_numeric_scaled = pd.DataFrame(X_scaled, columns=X.columns)
gdf_numeric_scaled['impact_score'] = y  # Add target column back for saving

# Add the original geometry column back to the DataFrame
gdf_numeric_scaled['geometry'] = gdf['geometry']  # Ensure 'geometry' column is retained

# Convert back to GeoDataFrame
gdf_numeric_scaled = gpd.GeoDataFrame(gdf_numeric_scaled, geometry='geometry')

# Save it as GeoJSON
output_path = '../feature_engineering/feature_engineering_glacier_lake_data_numeric_only.geojson'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

gdf_numeric_scaled.to_file(output_path, driver='GeoJSON')

print(f"\n✅ Feature engineered data with numeric-only values and 'impact_score' saved at {output_path}")
