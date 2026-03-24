import pandas as pd
import streamlit as st

@st.cache_data
def carregar_microdados():
    df = pd.read_csv("dados/tratado/enem_tratado_sample.csv")
    return df