import pandas as pd
import os
import streamlit as st

DATA_PATH = "../data/processed/dailyclimate_cleaned.csv"

@st.cache_data
def load_and_process_data():
    if not os.path.exists(DATA_PATH):
        return pd.DataFrame()

    df = pd.read_csv(DATA_PATH, parse_dates=['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    return df
