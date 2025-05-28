# import streamlit as st
# import datetime

# st.title("🌎 Climate Prediction and Assessment App")

# # --- Model selection ---
# model_choice = st.selectbox("Choose Model", [
#     'Ridge Regression',
#     'Lasso Regression',
#     'Gradient Boosting Regression',
#     'Random Forest Classifier',
#     'Support Vector Machine'
# ])

# # --- Hyperparameters ---
# params = {}
# run_fast = st.checkbox("⚡ Run Fast Mode", value=True)

# if model_choice in ["Ridge Regression", "Lasso Regression"]:
#     params['alpha'] = st.slider("Alpha", 0.01, 10.0, 1.0)
# elif model_choice == "Gradient Boosting Regression":
#     params['n_estimators'] = st.slider("Estimators", 50, 1000, 100)
#     params['learning_rate'] = st.slider("Learning Rate", 0.01, 0.5, 0.1)
#     params['max_depth'] = st.slider("Max Depth", 2, 10, 3)
# elif model_choice == "Random Forest Classifier":
#     params['n_estimators'] = st.slider("Estimators", 50, 500, 100)
# elif model_choice == "Support Vector Machine":
#     params['C'] = st.slider("Penalty (C)", 0.01, 10.0, 1.0)

# if st.button("🚀 Train and Predict"):
#     st.write("Training model...")

# # --- Future Prediction ---
# st.subheader("📅 Set Future Prediction Date")

# future_year = st.slider("Predict Year", 2025, 2035, 2026)
# future_month = st.selectbox("Predict Month", range(1, 13))
# future_day = st.slider("Predict Day", 1, 28, 15)

# if st.button("📅 Make Future Predictions"):
#     st.write("Making prediction for selected date...")

# import streamlit as st
# import datetime
# import pandas as pd
# import numpy as np
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.linear_model import LogisticRegression, Ridge, Lasso
# from sklearn.svm import SVC
# from sklearn.metrics import classification_report, confusion_matrix
# import joblib
# import os

# # --- App Title ---
# st.title("🌎 Climate Prediction and Assessment App")

# # --- Model selection ---
# model_choice = st.selectbox("Choose Model", [
#     'Random Forest Classifier',
#     'Logistic Regression',
#     'Support Vector Machine'
# ])


# # --- Hyperparameters ---
# params = {}
# run_fast = st.checkbox("⚡ Run Fast Mode", value=True)

# if model_choice in ["Ridge Regression", "Lasso Regression"]:
#     params['alpha'] = st.slider("Alpha", 0.01, 10.0, 1.0)
# elif model_choice == "Gradient Boosting Regression":
#     params['n_estimators'] = st.slider("Estimators", 50, 1000, 100)
#     params['learning_rate'] = st.slider("Learning Rate", 0.01, 0.5, 0.1)
#     params['max_depth'] = st.slider("Max Depth", 2, 10, 3)
# elif model_choice == "Random Forest Classifier":
#     params['n_estimators'] = st.slider("Estimators", 50, 500, 100)
# elif model_choice == "Support Vector Machine":
#     params['C'] = st.slider("Penalty (C)", 0.01, 10.0, 1.0)

# if st.button("🚀 Train and Predict"):
#     st.write("Training model...")

#     # Load and preprocess data
#     def load_and_preprocess_data(file_path):
#         df = pd.read_csv(file_path)

#         if 'disaster_type' in df.columns:
#             df = df.dropna(subset=['disaster_type'])

#         df['date'] = pd.to_datetime(df['date'])
#         df["disno"] = df["disno"].astype(str)

#         label_mapping = {label: idx for idx, label in enumerate(df['disaster_type'].unique())}
#         df['target'] = df['disaster_type'].map(label_mapping)

#         feature_cols = [
#             'latitude', 'longitude', 'temperature_avg', 'precipitation',
#             'precip_rolling_30d_mean', 'precip_rolling_30d_std', 'spi_like',
#             'heat_stress_index', 'is_monsoon', 'temp_lag_1', 'precip_lag_1',
#             'temp_lag_3', 'precip_lag_3', 'temp_lag_7', 'precip_lag_7',
#             'temp_lag_30', 'precip_lag_30', 'distance_to_center_km',
#             'pca_1', 'pca_2', 'pca_3', 'pca_4', 'pca_5',
#             'pca_6', 'pca_7', 'pca_8', 'pca_9', 'pca_10'
#         ]

#         X = df[feature_cols]
#         y = df['target']

#         # Remove extremely rare classes
#         class_counts = y.value_counts()
#         valid_classes = class_counts[class_counts >= 4].index
#         mask = y.isin(valid_classes)
#         X = X[mask]
#         y = y[mask]

#         # No SMOTE here
#         return X, y

#     file_path = 'path_to_data.csv'  # Update this path accordingly
#     X, y = load_and_preprocess_data(file_path)

#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#     # --- Model Training ---
#     scaler = StandardScaler()
#     X_train_scaled = scaler.fit_transform(X_train)
#     X_test_scaled = scaler.transform(X_test)

#     # Train model based on user selection
#     if model_choice == 'Random Forest Classifier':
#         model = RandomForestClassifier(
#             n_estimators=params['n_estimators'],
#             max_depth=10,
#             n_jobs=-1,
#             random_state=42,
#             class_weight='balanced'  # 🔥 Added for imbalance
#         )
#     elif model_choice == 'Ridge Regression':
#         model = Ridge(alpha=params['alpha'])
#     elif model_choice == 'Lasso Regression':
#         model = Lasso(alpha=params['alpha'])
#     elif model_choice == 'Gradient Boosting Regression':
#         from sklearn.ensemble import GradientBoostingRegressor
#         model = GradientBoostingRegressor(
#             n_estimators=params['n_estimators'],
#             learning_rate=params['learning_rate'],
#             max_depth=params['max_depth']
#         )
#     elif model_choice == 'Support Vector Machine':
#         model = SVC(
#             C=params['C'],
#             random_state=42,
#             class_weight='balanced'  # 🔥 Added for imbalance
#         )

#     model.fit(X_train_scaled, y_train)
#     y_pred = model.predict(X_test_scaled)

#     # --- Model Evaluation ---
#     classification_report_str = classification_report(y_test, y_pred)
#     confusion_matrix_str = confusion_matrix(y_test, y_pred)

#     st.write("Classification Report:")
#     st.text(classification_report_str)

#     st.write("Confusion Matrix:")
#     st.text(confusion_matrix_str)

#     # --- Save the model ---
#     model_dir = 'models/weather_climate_model/'
#     if not os.path.exists(model_dir):
#         os.makedirs(model_dir)

#     model_path = os.path.join(model_dir, f'{model_choice.lower().replace(" ", "_")}_model.pkl')
#     joblib.dump(model, model_path)
#     st.success(f"✅ Model saved at: {model_path}")

# # --- Future Prediction Section ---
# st.subheader("📅 Set Future Prediction Date")

# future_year = st.slider("Predict Year", 2025, 2035, 2026)
# future_month = st.selectbox("Predict Month", range(1, 13))
# future_day = st.slider("Predict Day", 1, 28, 15)

# if st.button("📅 Make Future Predictions"):
#     st.write("Making prediction for selected date...")
#     st.info(f"Prediction for {future_month}/{future_day}/{future_year} - (Example output)")


# import streamlit as st
# import datetime
# import pandas as pd
# import numpy as np
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.linear_model import LogisticRegression
# from sklearn.svm import SVC
# from sklearn.metrics import classification_report, confusion_matrix
# import joblib
# import os

# # --- App Title ---
# st.title("🌎 Climate Prediction and Assessment App")

# # --- Model selection ---
# model_choice = st.selectbox("Choose Model", [
#     'Random Forest Classifier',
#     'Logistic Regression',
#     'Support Vector Machine'
# ])

# run_fast = st.checkbox("⚡ Run Fast Mode", value=True)

# if st.button("🚀 Train and Predict"):
#     st.write("Training model...")

#     # --- Load and preprocess data ---
#     def load_and_preprocess_data(file_path):
#         df = pd.read_csv(file_path)

#         if 'disaster_type' in df.columns:
#             df = df.dropna(subset=['disaster_type'])

#         df['date'] = pd.to_datetime(df['date'])
#         df["disno"] = df["disno"].astype(str)

#         label_mapping = {label: idx for idx, label in enumerate(df['disaster_type'].unique())}
#         df['target'] = df['disaster_type'].map(label_mapping)

#         feature_cols = [
#             'latitude', 'longitude', 'temperature_avg', 'precipitation',
#             'precip_rolling_30d_mean', 'precip_rolling_30d_std', 'spi_like',
#             'heat_stress_index', 'is_monsoon', 'temp_lag_1', 'precip_lag_1',
#             'temp_lag_3', 'precip_lag_3', 'temp_lag_7', 'precip_lag_7',
#             'temp_lag_30', 'precip_lag_30', 'distance_to_center_km',
#             'pca_1', 'pca_2', 'pca_3', 'pca_4', 'pca_5',
#             'pca_6', 'pca_7', 'pca_8', 'pca_9', 'pca_10'
#         ]

#         X = df[feature_cols]
#         y = df['target']

#         # Remove rare classes
#         class_counts = y.value_counts()
#         valid_classes = class_counts[class_counts >= 4].index
#         mask = y.isin(valid_classes)
#         X = X[mask]
#         y = y[mask]

#         return X, y

#     # file_path = '../src/'  # ❗ Replace this with your actual CSV path
#     current_dir = os.path.dirname(os.path.abspath(__file__))
# csv_path = os.path.join(current_dir, '..', 'data', 'feature_engineering', 'engineered_weather_data.csv')

# if not os.path.exists(csv_path):
#     st.error(f"❗ Data file not found at expected location: `{csv_path}`")
#     st.stop()

# df, X, y = load_data(csv_path)
# if df is None:
#     st.stop()
#     X, y = load_and_preprocess_data(file_path)

#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#     # --- Feature Scaling ---
#     scaler = StandardScaler()
#     X_train_scaled = scaler.fit_transform(X_train)
#     X_test_scaled = scaler.transform(X_test)

#     # --- Train model based on selection ---
#     if model_choice == 'Random Forest Classifier':
#         model = RandomForestClassifier(
#             n_estimators=50,
#             max_depth=10,
#             n_jobs=-1,
#             random_state=42,
#             class_weight='balanced'
#         )
#     elif model_choice == 'Logistic Regression':
#         model = LogisticRegression(
#             max_iter=200,
#             solver='lbfgs',
#             multi_class='auto',
#             class_weight='balanced',
#             random_state=42
#         )
#     elif model_choice == 'Support Vector Machine':
#         model = SVC(
#             kernel='linear',
#             C=0.5,
#             probability=True,
#             class_weight='balanced',
#             random_state=42
#         )

#     model.fit(X_train_scaled, y_train)
#     y_pred = model.predict(X_test_scaled)

#     # --- Model Evaluation ---
#     st.write("Classification Report:")
#     st.text(classification_report(y_test, y_pred))

#     st.write("Confusion Matrix:")
#     st.text(confusion_matrix(y_test, y_pred))

#     # --- Save the model ---
#     model_dir = 'models/weather_climate_model/'
#     if not os.path.exists(model_dir):
#         os.makedirs(model_dir)

#     model_path = os.path.join(model_dir, f'{model_choice.lower().replace(" ", "_")}_model.pkl')
#     joblib.dump(model, model_path)
#     st.success(f"✅ Model saved at: {model_path}")

# # --- Future Prediction Section ---
# st.subheader("📅 Set Future Prediction Date")

# future_year = st.slider("Predict Year", 2025, 2035, 2026)
# future_month = st.selectbox("Predict Month", range(1, 13))
# future_day = st.slider("Predict Day", 1, 28, 15)

# if st.button("📅 Make Future Predictions"):
#     st.write("Making prediction for selected date...")
#     st.info(f"Prediction for {future_month}/{future_day}/{future_year} - (Example output)")


# import streamlit as st
# import datetime
# import pandas as pd
# import numpy as np
# import os
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.linear_model import LogisticRegression
# from sklearn.svm import SVC
# from sklearn.metrics import classification_report, confusion_matrix
# import joblib

# # --- App Title ---
# st.title("🌎 Climate Prediction and Assessment App")

# # --- Model selection ---
# model_choice = st.selectbox("Choose Model", [
#     'Random Forest Classifier',
#     'Logistic Regression',
#     'Support Vector Machine'
# ])

# run_fast = st.checkbox("⚡ Run Fast Mode", value=True)

# # --- Load and preprocess data ---
# def load_and_preprocess_data(file_path):
#     df = pd.read_csv(file_path)

#     if 'disaster_type' in df.columns:
#         df = df.dropna(subset=['disaster_type'])

#     df['date'] = pd.to_datetime(df['date'])
#     df["disno"] = df["disno"].astype(str)

#     label_mapping = {label: idx for idx, label in enumerate(df['disaster_type'].unique())}
#     df['target'] = df['disaster_type'].map(label_mapping)

#     feature_cols = [
#         'latitude', 'longitude', 'temperature_avg', 'precipitation',
#         'precip_rolling_30d_mean', 'precip_rolling_30d_std', 'spi_like',
#         'heat_stress_index', 'is_monsoon', 'temp_lag_1', 'precip_lag_1',
#         'temp_lag_3', 'precip_lag_3', 'temp_lag_7', 'precip_lag_7',
#         'temp_lag_30', 'precip_lag_30', 'distance_to_center_km',
#         'pca_1', 'pca_2', 'pca_3', 'pca_4', 'pca_5',
#         'pca_6', 'pca_7', 'pca_8', 'pca_9', 'pca_10'
#     ]

#     X = df[feature_cols]
#     y = df['target']

#     # Remove rare classes
#     class_counts = y.value_counts()
#     valid_classes = class_counts[class_counts >= 4].index
#     mask = y.isin(valid_classes)
#     X = X[mask]
#     y = y[mask]

#     return X, y

# # --- Training ---
# if st.button("🚀 Train and Predict"):
#     st.write("Training model...")

#     # File path setup
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     csv_path = os.path.join(current_dir, '..', 'data', 'feature_engineering', 'engineered_weather_data.csv')

#     if not os.path.exists(csv_path):
#         st.error(f"❗ Data file not found at expected location: `{csv_path}`")
#         st.stop()

#     X, y = load_and_preprocess_data(csv_path)

#     # Split
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#     # Scaling
#     scaler = StandardScaler()
#     X_train_scaled = scaler.fit_transform(X_train)
#     X_test_scaled = scaler.transform(X_test)

#     # --- Train model based on selection ---
#     if model_choice == 'Random Forest Classifier':
#         model = RandomForestClassifier(
#             n_estimators=50,
#             max_depth=10,
#             n_jobs=-1,
#             random_state=42,
#             class_weight='balanced'
#         )
#     elif model_choice == 'Logistic Regression':
#         model = LogisticRegression(
#             max_iter=200,
#             solver='lbfgs',
#             multi_class='auto',
#             class_weight='balanced',
#             random_state=42
#         )
#     elif model_choice == 'Support Vector Machine':
#         model = SVC(
#             kernel='linear',
#             C=0.5,
#             probability=True,
#             class_weight='balanced',
#             random_state=42
#         )

#     model.fit(X_train_scaled, y_train)
#     y_pred = model.predict(X_test_scaled)

#     # --- Model Evaluation ---
#     st.write("Classification Report:")
#     st.text(classification_report(y_test, y_pred))

#     st.write("Confusion Matrix:")
#     st.text(confusion_matrix(y_test, y_pred))

#     # --- Save the model ---
#     model_dir = 'models/weather_climate_model/'
#     os.makedirs(model_dir, exist_ok=True)

#     model_path = os.path.join(model_dir, f'{model_choice.lower().replace(" ", "_")}_model.pkl')
#     joblib.dump(model, model_path)
#     st.success(f"✅ Model saved at: {model_path}")

# # # --- Future Prediction Section ---
# # st.subheader("📅 Set Future Prediction Date")

# # future_year = st.slider("Predict Year", 2025, 2035, 2026)
# # future_month = st.selectbox("Predict Month", range(1, 13))
# # future_day = st.slider("Predict Day", 1, 28, 15)

# # if st.button("📅 Make Future Predictions"):
# #     st.write("Making prediction for selected date...")
# #     st.info(f"Prediction for {future_month}/{future_day}/{future_year} - (Example output)")


# # --- Future Prediction Section ---
# st.subheader("📅 Set Future Prediction Date")

# future_year = st.slider("Predict Year", 2025, 2035, 2026)
# future_month = st.selectbox("Predict Month", range(1, 13))
# future_day = st.slider("Predict Day", 1, 28, 15)

# if st.button("📅 Make Future Predictions"):
#     st.write("Loading model and preparing features...")

#     # Load the trained model
#     model_path = os.path.join('models/weather_climate_model', f'{model_choice.lower().replace(" ", "_")}_model.pkl')
#     if not os.path.exists(model_path):
#         st.error("❌ Trained model not found. Please train the model first.")
#         st.stop()
#     model = joblib.load(model_path)

#     # Load data and preprocess
#     full_df = pd.read_csv(csv_path)

#     # Drop rows with missing target
#     full_df = full_df.dropna(subset=['disaster_type'])

#     # Prepare label mapping and features
#     label_mapping = {label: idx for idx, label in enumerate(full_df['disaster_type'].unique())}
#     reverse_mapping = {v: k for k, v in label_mapping.items()}
#     full_df['target'] = full_df['disaster_type'].map(label_mapping)

#     feature_cols = [
#         'latitude', 'longitude', 'temperature_avg', 'precipitation',
#         'precip_rolling_30d_mean', 'precip_rolling_30d_std', 'spi_like',
#         'heat_stress_index', 'is_monsoon', 'temp_lag_1', 'precip_lag_1',
#         'temp_lag_3', 'precip_lag_3', 'temp_lag_7', 'precip_lag_7',
#         'temp_lag_30', 'precip_lag_30', 'distance_to_center_km',
#         'pca_1', 'pca_2', 'pca_3', 'pca_4', 'pca_5',
#         'pca_6', 'pca_7', 'pca_8', 'pca_9', 'pca_10'
#     ]

#     X_full = full_df[feature_cols]
#     y_full = full_df['target']

#     # Fit the scaler
#     scaler = StandardScaler()
#     X_full_scaled = scaler.fit_transform(X_full)

#     # Use the most recent row of real data for prediction
#     future_features_scaled = X_full_scaled[-1].reshape(1, -1)

#     # Predict using the model
#     prediction = model.predict(future_features_scaled)[0]
#     predicted_label = reverse_mapping.get(prediction, "Unknown")

#     # Display prediction
#     future_date = f"{future_year}-{future_month:02d}-{future_day:02d}"
#     st.success(f"✅ Predicted Disaster Type on {future_date}: **{predicted_label}**")


# import streamlit as st
# import datetime
# import pandas as pd
# import numpy as np
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.linear_model import LogisticRegression
# from sklearn.svm import SVC
# from sklearn.metrics import classification_report, confusion_matrix
# import joblib
# import os

# # --- App Title ---
# st.title("🌎 Climate Prediction and Assessment App")

# # Get current file's directory
# current_dir = os.path.dirname(os.path.abspath(__file__))

# # Define csv_path globally
# csv_path = os.path.join(current_dir, '..', 'data', 'feature_engineering', 'engineered_weather_data.csv')

# # Optional check to ensure the data file exists
# if not os.path.exists(csv_path):
#     st.error(f"❗ Data file not found at expected location: `{csv_path}`")
#     st.stop()

# # --- Model selection ---
# model_choice = st.selectbox("Choose Model", [
#     'Random Forest Classifier',
#     'Logistic Regression',
#     'Support Vector Machine'
# ])

# run_fast = st.checkbox("⚡ Run Fast Mode", value=True)

# if st.button("🚀 Train and Predict"):
#     st.write("Training model...")

#     # --- Load and preprocess data ---
#     def load_and_preprocess_data(file_path):
#         df = pd.read_csv(file_path)

#         if 'disaster_type' in df.columns:
#             df = df.dropna(subset=['disaster_type'])

#         df['date'] = pd.to_datetime(df['date'])
#         df["disno"] = df["disno"].astype(str)

#         label_mapping = {label: idx for idx, label in enumerate(df['disaster_type'].unique())}
#         df['target'] = df['disaster_type'].map(label_mapping)

#         feature_cols = [
#             'latitude', 'longitude', 'temperature_avg', 'precipitation',
#             'precip_rolling_30d_mean', 'precip_rolling_30d_std', 'spi_like',
#             'heat_stress_index', 'is_monsoon', 'temp_lag_1', 'precip_lag_1',
#             'temp_lag_3', 'precip_lag_3', 'temp_lag_7', 'precip_lag_7',
#             'temp_lag_30', 'precip_lag_30', 'distance_to_center_km',
#             'pca_1', 'pca_2', 'pca_3', 'pca_4', 'pca_5',
#             'pca_6', 'pca_7', 'pca_8', 'pca_9', 'pca_10'
#         ]

#         X = df[feature_cols]
#         y = df['target']

#         # Remove rare classes
#         class_counts = y.value_counts()
#         valid_classes = class_counts[class_counts >= 4].index
#         mask = y.isin(valid_classes)
#         X = X[mask]
#         y = y[mask]

#         return X, y

#     # Load data
#     X, y = load_and_preprocess_data(csv_path)

#     # Split data into training and testing sets
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#     # --- Feature Scaling ---
#     scaler = StandardScaler()
#     X_train_scaled = scaler.fit_transform(X_train)
#     X_test_scaled = scaler.transform(X_test)

#     # --- Train model based on selection ---
#     if model_choice == 'Random Forest Classifier':
#         model = RandomForestClassifier(
#             n_estimators=50,
#             max_depth=10,
#             n_jobs=-1,
#             random_state=42,
#             class_weight='balanced'
#         )
#     elif model_choice == 'Logistic Regression':
#         model = LogisticRegression(
#             max_iter=200,
#             solver='lbfgs',
#             multi_class='auto',
#             class_weight='balanced',
#             random_state=42
#         )
#     elif model_choice == 'Support Vector Machine':
#         model = SVC(
#             kernel='linear',
#             C=0.5,
#             probability=True,
#             class_weight='balanced',
#             random_state=42
#         )

#     # Train the model
#     model.fit(X_train_scaled, y_train)
#     y_pred = model.predict(X_test_scaled)

#     # --- Model Evaluation ---
#     st.write("Classification Report:")
#     st.text(classification_report(y_test, y_pred))

#     st.write("Confusion Matrix:")
#     st.text(confusion_matrix(y_test, y_pred))

#     # --- Save the model ---
#     model_dir = 'models/weather_climate_model/'
#     if not os.path.exists(model_dir):
#         os.makedirs(model_dir)

#     model_path = os.path.join(model_dir, f'{model_choice.lower().replace(" ", "_")}_model.pkl')
#     joblib.dump(model, model_path)
#     st.success(f"✅ Model saved at: {model_path}")

# # --- Future Prediction Section ---
# # --- Set Future Prediction Date ---
# st.subheader("📅 Set Future Prediction Date")

# future_year = st.slider("Predict Year", 2025, 2035, 2026)
# future_month = st.selectbox("Predict Month", range(1, 13))
# future_day = st.slider("Predict Day", 1, 28, 15)

# # Define the disaster type mapping (assuming training set labels)
# disaster_types = {
#     0: "Flood",
#     1: "Drought",
#     2: "Earthquake",
#     3: "Cyclone",
#     4: "Wildfire",
#     5: "Landslide"
# }

# disaster_colors = {
#     "Flood": "blue",
#     "Drought": "yellow",
#     "Earthquake": "gray",
#     "Cyclone": "red",
#     "Wildfire": "orange",
#     "Landslide": "brown"
# }

# if st.button("📅 Make Future Predictions"):
#     st.write(f"Making prediction for {future_month}/{future_day}/{future_year}...")

#     # Load the CSV data
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     csv_path = os.path.join(current_dir, '..', 'data', 'feature_engineering', 'engineered_weather_data.csv')

#     if not os.path.exists(csv_path):
#         st.error(f"❗ Data file not found at expected location: `{csv_path}`")
#         st.stop()

#     df, X, y = load_and_preprocess_data(csv_path)

#     # Filter data for the desired prediction date
#     future_date = pd.to_datetime(f"{future_year}-{future_month}-{future_day}")
#     future_data = df[df['date'] == future_date]

#     if future_data.empty:
#         st.error(f"❗ No data available for the selected date: {future_date}")
#         st.stop()

#     # Get the features for the selected date (assuming only one row for simplicity)
#     future_features = future_data[[
#         'latitude', 'longitude', 'temperature_avg', 'precipitation',
#         'precip_rolling_30d_mean', 'precip_rolling_30d_std', 'spi_like',
#         'heat_stress_index', 'is_monsoon', 'temp_lag_1', 'precip_lag_1',
#         'temp_lag_3', 'precip_lag_3', 'temp_lag_7', 'precip_lag_7',
#         'temp_lag_30', 'precip_lag_30', 'distance_to_center_km',
#         'pca_1', 'pca_2', 'pca_3', 'pca_4', 'pca_5',
#         'pca_6', 'pca_7', 'pca_8', 'pca_9', 'pca_10'
#     ]]

#     # Load the trained model
#     model_path = 'models/weather_climate_model/random_forest_classifier_model.pkl'  # Adjust path as needed
#     model = joblib.load(model_path)

#     # Make prediction
#     prediction = model.predict(future_features)

#     # Get the predicted disaster type (human-readable)
#     predicted_disaster_type = disaster_types[prediction[0]]
#     disaster_color = disaster_colors.get(predicted_disaster_type, "gray")  # Default to gray if not found

#     # Show prediction with a cool, colorful message
#     st.markdown(f"<p style='color:{disaster_color}; font-size:20px;'>Predicted Disaster Type for {future_month}/{future_day}/{future_year}: <strong>{predicted_disaster_type}</strong></p>", unsafe_allow_html=True)


import streamlit as st
import datetime
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os

# --- App Title ---
st.title("🌎 Climate Prediction and Assessment App")

# Get current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define paths for data and models
data_dir = os.path.join(current_dir, '..', 'feature_engineering')
csv_path = os.path.join(data_dir, 'weather_and_temp_feature_engineering.csv')
model_dir = 'models/weather_climate_model/'

# Optional check to ensure the data file exists
if not os.path.exists(csv_path):
    st.error(f"❗ Data file not found at expected location: `{csv_path}`")
    st.stop()

# --- Model selection ---
model_choice = st.selectbox("Choose Model", [
    'Random Forest Classifier',
    'Logistic Regression',
    'Support Vector Machine'
])

run_fast = st.checkbox("⚡ Run Fast Mode", value=True)

# Function to load and preprocess the data
def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path)

    if 'disaster_type' in df.columns:
        df = df.dropna(subset=['disaster_type'])

    df['date'] = pd.to_datetime(df['date'])
    df["disno"] = df["disno"].astype(str)

    label_mapping = {label: idx for idx, label in enumerate(df['disaster_type'].unique())}
    df['target'] = df['disaster_type'].map(label_mapping)

    feature_cols = [
        'latitude', 'longitude', 'temperature_avg', 'precipitation',
        'precip_rolling_30d_mean', 'precip_rolling_30d_std', 'spi_like',
        'heat_stress_index', 'is_monsoon', 'temp_lag_1', 'precip_lag_1',
        'temp_lag_3', 'precip_lag_3', 'temp_lag_7', 'precip_lag_7',
        'temp_lag_30', 'precip_lag_30', 'distance_to_center_km',
        'pca_1', 'pca_2', 'pca_3', 'pca_4', 'pca_5',
        'pca_6', 'pca_7', 'pca_8', 'pca_9', 'pca_10'
    ]

    X = df[feature_cols]
    y = df['target']

    # Remove rare classes
    class_counts = y.value_counts()
    valid_classes = class_counts[class_counts >= 4].index
    mask = y.isin(valid_classes)
    X = X[mask]
    y = y[mask]

    return X, y, df

# --- Train and Predict ---
if st.button("🚀 Train and Predict"):
    st.write("Training model...")

    # Load and preprocess data
    X, y, _ = load_and_preprocess_data(csv_path)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # --- Feature Scaling ---
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # --- Train model based on selection ---
    if model_choice == 'Random Forest Classifier':
        model = RandomForestClassifier(
            n_estimators=50,
            max_depth=10,
            n_jobs=-1,
            random_state=42,
            class_weight='balanced'
        )
    elif model_choice == 'Logistic Regression':
        model = LogisticRegression(
            max_iter=200,
            solver='lbfgs',
            multi_class='auto',
            class_weight='balanced',
            random_state=42
        )
    elif model_choice == 'Support Vector Machine':
        model = SVC(
            kernel='linear',
            C=0.5,
            probability=True,
            class_weight='balanced',
            random_state=42
        )

    # Train the model
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)

    # --- Model Evaluation ---
    st.write("Classification Report:")
    st.text(classification_report(y_test, y_pred))

    st.write("Confusion Matrix:")
    st.text(confusion_matrix(y_test, y_pred))

    # --- Save the model ---
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    model_path = os.path.join(model_dir, f'{model_choice.lower().replace(" ", "_")}_model.pkl')
    joblib.dump(model, model_path)
    # st.success(f"✅ Model saved at: {model_path}")

# --- Future Prediction Section ---
# --- Future Prediction Section ---
st.subheader("📅 Set Future Prediction Date")

future_year = st.slider("Predict Year", 2025, 2035, 2026)
future_month = st.selectbox("Predict Month", range(1, 13))
future_day = st.slider("Predict Day", 1, 28, 15)

# Define the disaster type mapping (assuming training set labels)
disaster_types = {
    0: "Flood",
    1: "Drought",
    2: "Earthquake",
    3: "Cyclone",
    4: "Wildfire",
    5: "Landslide"
}

disaster_colors = {
    "Flood": "blue",
    "Drought": "yellow",
    "Earthquake": "gray",
    "Cyclone": "red",
    "Wildfire": "orange",
    "Landslide": "brown"
}

if st.button("📅 Make Future Predictions"):
    st.write(f"Making prediction for {future_month}/{future_day}/{future_year}...")

    # Load data
    _, _, df = load_and_preprocess_data(csv_path)

    # Normalize the 'date' column to strip the time part (if any)
    df['date'] = pd.to_datetime(df['date']).dt.normalize()

    # Create the future prediction date and normalize it
    future_date = pd.to_datetime(f"{future_year}-{future_month}-{future_day}").normalize()

    # Debug: print to check both normalized date columns
    st.write(f"Future date selected: {future_date}")
    # st.write(f"Sample dates in dataset (first 5 rows):")
    # st.write(df['date'].head())

    # Find the closest available date if no exact match is found
    closest_date = df.iloc[(df['date'] - future_date).abs().argmin()]['date']
    # st.write(f"Closest available date in dataset: {closest_date}")

    # Filter data for the closest available date
    future_data = df[df['date'] == closest_date]

    # Get the features for the closest available date (assuming only one row for simplicity)
    future_features = future_data[[
        'latitude', 'longitude', 'temperature_avg', 'precipitation',
        'precip_rolling_30d_mean', 'precip_rolling_30d_std', 'spi_like',
        'heat_stress_index', 'is_monsoon', 'temp_lag_1', 'precip_lag_1',
        'temp_lag_3', 'precip_lag_3', 'temp_lag_7', 'precip_lag_7',
        'temp_lag_30', 'precip_lag_30', 'distance_to_center_km',
        'pca_1', 'pca_2', 'pca_3', 'pca_4', 'pca_5',
        'pca_6', 'pca_7', 'pca_8', 'pca_9', 'pca_10'
    ]]

    # Load the trained model
    model_path = os.path.join(model_dir, 'random_forest_classifier_model.pkl')
    model = joblib.load(model_path)

    # Make prediction
    prediction = model.predict(future_features)

    # Get the predicted disaster type (human-readable)
    predicted_disaster_type = disaster_types[prediction[0]]
    disaster_color = disaster_colors.get(predicted_disaster_type, "gray")  # Default to gray if not found

    # Show prediction with a cool, colorful message
    st.markdown(f"<p style='color:{disaster_color}; font-size:20px;'>Predicted Disaster Type for {future_month}/{future_day}/{future_year}: <strong>{predicted_disaster_type}</strong></p>", unsafe_allow_html=True)
