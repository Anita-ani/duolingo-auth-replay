import streamlit as st
import pandas as pd
import requests

st.title("SentinelGrid – Network Anomaly Dashboard")

if st.button("Detect Anomalies"):
    res = requests.get("http://localhost:8000/detect")
    if res.status_code == 200:
        df = pd.DataFrame(res.json())
        st.dataframe(df)
    else:
        st.error("Failed to retrieve anomalies.")
