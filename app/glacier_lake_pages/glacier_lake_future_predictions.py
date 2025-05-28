
# glacier_lake_future_predictions.py

import streamlit as st
import os
import sys
import pandas as pd
import numpy as np
import geopandas as gpd
import joblib
import matplotlib.pyplot as plt

# --- Setup Paths ---
current_dir = os.path.dirname(os.path.abspath(__file__))  # app/
root_dir = os.path.dirname(current_dir)
src_dir = os.path.join(root_dir, 'src')
models_dir = os.path.join(current_dir, 'models', 'glacier_data_model')
data_file = os.path.join(root_dir, 'data', 'processed', 'combined_data.geojson')

if src_dir not in sys.path:
    sys.path.append(src_dir)

# --- Import Training Function ---
try:
    from glacier_lake_model_training import train_glacier_lake_models
except ImportError as e:
    st.error(f"Error loading training module: {e}")
    st.stop()

# --- Helper Functions ---
@st.cache_data
def load_data(source):
    """Load data from a file path or uploaded file."""
    try:
        if isinstance(source, str):
            if source.endswith('.csv'):
                return pd.read_csv(source)
            elif source.endswith('.geojson'):
                return gpd.read_file(source)
        elif hasattr(source, 'name'):
            if source.name.endswith('.csv'):
                return pd.read_csv(source)
            elif source.name.endswith('.geojson'):
                return gpd.read_file(source)
        st.error("Unsupported file format.")
        return None
    except Exception as e:
        st.error(f"Error reading data: {e}")
        return None

def load_model(model_name):
    """Load a model from disk."""
    path = os.path.join(models_dir, f"{model_name}.joblib")
    if os.path.exists(path):
        return joblib.load(path)
    st.error(f"❌ Model `{model_name}` not found at {path}.")
    return None

@st.cache_resource
def load_all_models():
    """Load all classification and regression models."""
    classification_models = {
        name: load_model(name) for name in [
            'random_forest_climate_zone',
            'svm_extreme_event',
            'gradient_boosting_vulnerability_level'
        ]
    }
    regression_models = {
        name: load_model(name) for name in [
            'linear_regression_impact_score',
            'ridge_regression_impact_score',
            'lasso_regression_impact_score',
            'gradient_boosting_regression_impact_score'
        ]
    }
    return classification_models, regression_models

def preprocess_features(df):
    """Preprocess features to match training format."""
    drop_columns = ['asso_glac', 'basin', 'country', 'datasource', 'drain_cond', 'geometry', 'target_column']
    df = df.drop(columns=[col for col in drop_columns if col in df.columns], errors='ignore')
    df = df.select_dtypes(include=[np.number])
    df = df.fillna(df.mean())
    return df

def make_predictions(models, features):
    """Use loaded models to make predictions."""
    results = {}
    for model_name, model in models.items():
        if model:
            try:
                results[model_name] = model.predict(features)
            except Exception as e:
                st.error(f"Prediction error with `{model_name}`: {e}")
    return results

def show_classification_insights(predictions, model_name):
    """Display insights for classification model."""
    df_preds = pd.DataFrame({f"{model_name} Prediction": predictions})
    counts = df_preds[f"{model_name} Prediction"].value_counts()

    # Show Table
    st.write(f"### 🔢 {model_name} - Value Counts")
    st.dataframe(counts)

    # Show Bar Chart
    fig, ax = plt.subplots()
    counts.plot(kind='bar', color='teal', ax=ax)
    plt.title(f"{model_name} Prediction Distribution")
    plt.xlabel("Predicted Class")
    plt.ylabel("Count")
    st.pyplot(fig)

    # CSV Download
    csv = df_preds.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"📥 Download {model_name} Predictions CSV",
        data=csv,
        file_name=f"{model_name}_predictions.csv",
        mime='text/csv'
    )

def show_regression_insights(predictions, model_name):
    """Display insights for regression model."""
    df_preds = pd.DataFrame({f"{model_name} Prediction": predictions})

    st.write(f"### 📈 {model_name} - Prediction Summary")
    st.dataframe(df_preds.describe())

    # Histogram Plot
    fig, ax = plt.subplots()
    df_preds.hist(bins=30, color='orange', ax=ax)
    plt.title(f"{model_name} Predictions Distribution")
    plt.xlabel("Predicted Value")
    plt.ylabel("Frequency")
    st.pyplot(fig)

    # CSV Download
    csv = df_preds.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"📥 Download {model_name} Predictions CSV",
        data=csv,
        file_name=f"{model_name}_predictions.csv",
        mime='text/csv'
    )

# --- Streamlit App ---
st.title("🧊 Glacier Lake Future Predictions")
st.markdown("Train models, load saved models, predict glacier lake behaviors, and visualize insights.")

# --- Section 1: Model Training ---
st.header("⚙️ Model Training")
if st.button("🚀 Train Glacier Lake Models"):
    with st.spinner("Training models... please wait..."):
        result = train_glacier_lake_models()
        st.success("✅ Training completed successfully!")
        st.markdown("### 🏷 Models Trained:")
        st.markdown("- Classification: `random_forest_climate_zone`, `svm_extreme_event`, `gradient_boosting_vulnerability_level`")
        st.markdown("- Regression: `linear_regression_impact_score`, `ridge_regression_impact_score`, `lasso_regression_impact_score`, `gradient_boosting_regression_impact_score`")
        st.markdown(f"📂 Models saved in: `{result['models_saved_in']}`")

# --- Section 2: Model Loading ---
st.header("📂 Model Loading")
if st.button("📥 Load Trained Models"):
    classification_models, regression_models = load_all_models()
    if all(classification_models.values()) and all(regression_models.values()):
        st.success("✅ All models loaded successfully!")
        st.session_state['classification_models'] = classification_models
        st.session_state['regression_models'] = regression_models
    else:
        st.warning("⚠️ Some models failed to load. Please retrain if needed.")

# --- Section 3: Prediction ---
if 'classification_models' in st.session_state and 'regression_models' in st.session_state:
    st.header("🔮 Predictions on Internal Dataset")

    data = load_data(data_file)

    if data is not None:
        st.success(f"✅ Loaded dataset: `{os.path.basename(data_file)}`")
        st.dataframe(data.head())

        features = preprocess_features(data)

        if st.button("🔎 Predict on Internal Data"):
            with st.spinner("Making predictions..."):
                # --- Classification Predictions ---
                st.subheader("🔵 Classification Predictions")
                classification_results = make_predictions(st.session_state['classification_models'], features)
                for model_name, preds in classification_results.items():
                    # st.write(f"## 📄 {model_name}")
                    show_classification_insights(preds, model_name)

                # --- Regression Predictions ---
                st.subheader("🟣 Regression Predictions")
                regression_results = make_predictions(st.session_state['regression_models'], features)
                for model_name, preds in regression_results.items():
                    # st.write(f"## 📄 {model_name}")
                    show_regression_insights(preds, model_name)

    else:
        st.error("❌ Failed to load internal dataset. Check the path or file.")
else:
    st.info("ℹ️ Please load models before making predictions.")
