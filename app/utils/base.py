import streamlit as st
import os

# Set page configuration at the very beginning of the main app (Home.py)
st.set_page_config(page_title="Climate Impact Nepal", layout="wide")

# Initialize session state if it doesn't already exist
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "climate_selection" not in st.session_state:
    st.session_state.climate_selection = "Select..."
if "glacier_selection" not in st.session_state:
    st.session_state.glacier_selection = "Select..."
if "socio_economic_selection" not in st.session_state:
    st.session_state.socio_economic_selection = "Select..."

# Sidebar layout
st.sidebar.markdown("### Main")  # Title for the main section

# Home button to reset to Home page
if st.sidebar.button("🏠 Home"):
    st.session_state.page = "Home"
    st.session_state.climate_selection = "Select..."
    st.session_state.glacier_selection = "Select..."
    st.session_state.socio_economic_selection = "Select..."

# Sidebar navigation sections
st.sidebar.markdown("### Navigations")

# Climate Pages
climate_pages = [
    "Climate Data - Vulnerability",
    "Climate Data - Analysis",
    "Climate Data - Predictions"
]

# Fix: Correct index calculation for climate selectbox
climate_index = 0 if st.session_state.climate_selection == "Select..." else climate_pages.index(st.session_state.climate_selection) + 1

selected_climate = st.sidebar.selectbox(
    "Climate Sections",
    ["Select..."] + climate_pages,
    index=climate_index,
    key="climate_selection"
)
if selected_climate in climate_pages:
    st.session_state.page = selected_climate

# Glacier Pages
st.sidebar.markdown("### Glacier Data")  # Title for Glacier section
glacier_pages = [
    "Glacier Data - Overview",
    "Glacier Data - Trends"
]

# Fix: Correct index calculation for glacier selectbox
glacier_index = 0 if st.session_state.glacier_selection == "Select..." else glacier_pages.index(st.session_state.glacier_selection) + 1

selected_glacier = st.sidebar.selectbox(
    "Glacier Data",
    ["Select..."] + glacier_pages,
    index=glacier_index,
    key="glacier_selection"
)

# Socio-Economic Pages
st.sidebar.markdown("### Socio-Economic Impact")  # Title for Socio-Economic section
socio_economic_pages = [
    "Socio-Economic Impact - Overview",
    "Socio-Economic Impact - Trends"
]

# Fix: Correct index calculation for socio-economic selectbox
socio_economic_index = 0 if st.session_state.socio_economic_selection == "Select..." else socio_economic_pages.index(st.session_state.socio_economic_selection) + 1

selected_socio_economic = st.sidebar.selectbox(
    "Socio-Economic Impact",
    ["Select..."] + socio_economic_pages,
    index=socio_economic_index,
    key="socio_economic_selection"
)

# File mapping for page execution (currently no real pages, just placeholders)
PAGES = {
    "Climate Data - Vulnerability": "climate_pages/1_Vulnerability.py",
    "Climate Data - Analysis": "climate_pages/2_Analysis.py",
    "Climate Data - Predictions": "climate_pages/3_Predictions.py",
    "Glacier Data - Overview": "",  # Dummy page
    "Glacier Data - Trends": "",  # Dummy page
    "Socio-Economic Impact - Overview": "",  # Dummy page
    "Socio-Economic Impact - Trends": ""  # Dummy page
}

# Render selected page
if st.session_state.page == "Home":
    st.write("""
    ### App Overview:
    This app is designed to help monitor, analyze, and predict climate impacts, with a focus on Nepal's climate data. 

    Key Features:
    - **Vulnerability Analysis**: Identifies regions most at risk due to extreme climate conditions like high temperatures and precipitation.
    - **Climate Data Analysis**: Analyzes trends and detects outliers in climate data such as temperature and precipitation.
    - **Temperature Predictions**: Uses machine learning to forecast future temperature trends based on historical data.
    - **Glacier Data**: (Coming soon) Explore glacier melt trends and their impact on water resources.
    - **Socio-Economic Impact**: (Coming soon) Analyze how climate change affects livelihoods, migration, and economy.

    Each section offers interactive charts, data analysis, and predictive models to better understand the climate change impact.
    """)
else:
    # For now, these pages are placeholders, so no actual code execution.
    if st.session_state.page in PAGES:
        if PAGES[st.session_state.page]:
            page_path = PAGES[st.session_state.page]
            with open(page_path, "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()
                exec(code, globals())
        else:
            st.write(f"{st.session_state.page} is a dummy page.")
    else:
        st.error(f"Page `{st.session_state.page}` not found.")
