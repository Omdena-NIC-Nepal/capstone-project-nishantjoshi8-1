import streamlit as st
import os
import pandas as pd

# --- Initialize session state ---
if "main_section" not in st.session_state:
    st.session_state.main_section = "Select..."
if "sub_page" not in st.session_state:
    st.session_state.sub_page = "Select..."
if "page" not in st.session_state:
    st.session_state.page = "Home"

# --- Sidebar Layout ---
st.sidebar.markdown("### 🧭 Main Navigation")

# Main Sections
main_sections = ["Climate Sections", "Weather Sections", "Glacier Lake Data", "Socio-Economic Impact"]

# Subpages Mapping
subpages_mapping = {
    "Climate Sections": [
        "Climate Data - Vulnerability",
        "Climate Data - Analysis",
        "Climate Data - Predictions"
    ],
    "Weather Sections": [
        "Weather Data Visualization",
        "Weather Impact Assessment",
        "Weather Predictions"
    ],
    "Glacier Lake Data": [
        "Glacier Lake Mapping & Visualization",
        "Glacier Lake Impact Assessment",
        "Glacier Lake Future Predictions"
    ],
    "Socio-Economic Impact": [
        "Socio-Economic Impact - Overview",
        "Socio-Economic Impact - Trends"
    ]
}

# NLP Sections
nlp_sections = [
    "Language Prediction",
    "NER Prediction",
    "Sentiment Analysis",
    "Summary Details",
]

# File Mapping
PAGES = {
    "Climate Data - Vulnerability": "climate_pages/1_Vulnerability.py",
    "Climate Data - Analysis": "climate_pages/2_Analysis.py",
    "Climate Data - Predictions": "climate_pages/3_Predictions.py",
    "Glacier Lake Mapping & Visualization": "glacier_lake_pages/glacier_lake_mapping_visualization.py",
    "Glacier Lake Impact Assessment": "glacier_lake_pages/glacier_lake_impact_assessment.py",
    "Glacier Lake Future Predictions": "glacier_lake_pages/glacier_lake_future_predictions.py",
    "Weather Data Visualization": "weather_pages/weather_data_visualization.py",
    "Weather Impact Assessment": "weather_pages/weather_impact_assesment.py",
    "Weather Predictions": "weather_pages/weather_predictions.py",
    "Socio-Economic Impact - Overview": "",
    "Socio-Economic Impact - Trends": "",
    "Sentiment Analysis": "nlp_pages/sentiment_analysis.py",
    "Language Prediction": "nlp_pages/language_prediction.py",
    "NER Prediction": "nlp_pages/ner_prediction.py",
    "Summary Details": "nlp_pages/summary_details.py",
}

# --- Home Button ---
if st.sidebar.button("🏡 Go to Home"):
    st.session_state.main_section = "Select..."
    st.session_state.sub_page = "Select..."
    st.session_state.page = "Home"

# --- Main Section Selection ---
selected_main = st.sidebar.selectbox(
    "🗂️ Select Section",
    ["Select..."] + main_sections,
    index=0,
    key="main_section"
)

# --- Subpage Selection ---
if selected_main != "Select...":
    available_subpages = subpages_mapping[selected_main]
    selected_subpage = st.sidebar.selectbox(
        f"📄 Select {selected_main} Page",
        ["Select..."] + available_subpages,
        index=0,
        key="sub_page"
    )
    if selected_subpage in PAGES:
        st.session_state.page = selected_subpage

# --- Conditional District Dropdown for Weather Pages ---
if st.session_state.page in ["Weather Data Visualization", "Weather Impact Assessment"]:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.abspath(os.path.join(BASE_DIR, '../feature_engineering/weather_and_temp_feature_engineering.csv'))
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        districts = df['district'].dropna().unique().tolist()
        selected_district = st.sidebar.selectbox("🏞️ Select District", ['All'] + districts)
        if selected_district != 'All':
            df = df[df['district'] == selected_district]
    else:
        st.sidebar.error("⚠️ Weather data file not found.")

# --- NLP Section ---
st.sidebar.markdown("---")
st.sidebar.markdown("### 🧠 NLP Tools")
selected_nlp = st.sidebar.selectbox(
    "🤖 Select NLP Section",
    ["Select..."] + nlp_sections,
    index=0,
    key="nlp_section"
)
if selected_nlp != "Select...":
    st.session_state.page = selected_nlp

# --- Page Display Logic ---
if st.session_state.page == "Home":

    # Add background watermark style
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("public/nepal_map_watermark.png");
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
            background-size: 60%;
            opacity: 0.95;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.write("""
    ### 🌍 Climate Prediction and Assessment App
    Welcome to the app! 
    Use the sidebar to explore different sections.

    **Key Features:**
    - 📊 Vulnerability Analysis
    - 📈 Climate Trend Analysis
    - 🌦️ Weather Visualizations and Predictions
    - 🧊 Glacier Lake Mapping and Risk Assessment
    - 🏘️ Socio-Economic Impact Evaluation *(Coming Soon!)* 
    - 🧠 NLP Tools for Language, Sentiment, NER & Summarization
    """)

    st.markdown("---")
    st.info("ℹ️ Tip: Refresh the browser if redirection doesn't work properly.")

else:
    page_path = PAGES.get(st.session_state.page, None)
    if page_path:
        try:
            base_dir = os.path.dirname(__file__)
            abs_path = os.path.join(base_dir, page_path)

            if os.path.exists(abs_path):
                with open(abs_path, "r", encoding="utf-8", errors="ignore") as f:
                    code = f.read()
                    exec(code, globals())
            else:
                st.error(f"❌ File not found at: {abs_path}")
        except Exception as e:
            st.error(f"🚨 Error loading `{st.session_state.page}`: {str(e)}")
    else:
        st.info(f"🚧 Page `{st.session_state.page}` is a placeholder and will be available soon.")
