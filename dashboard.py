import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

st.set_page_config(page_title="Air Quality Dashboard", layout="centered")
st.title("Real-Time Air Quality Monitoring")

DATA_FILE = "data/air_quality_log.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df
    else:
        return pd.DataFrame(columns=["timestamp", "value"])

df = load_data()

if df.empty:
    st.warning("No data received yet from ESP32.")
else:
    fig = px.line(df, x="timestamp", y="value", title="Gas Sensor Voltage Over Time")
    st.plotly_chart(fig, use_container_width=True)

    latest_val = df["value"].iloc[-1]
    st.metric("Latest Voltage", f"{latest_val:.2f} V")

    if latest_val > 2.0:
        st.error("Air Quality Unsafe!")
    elif latest_val > 1.5:
        st.warning("Moderate Air Quality")
    else:
        st.success("✅ Air Quality Safe")
    
    st.download_button(                                        #dowload csv file
        label="Download Air Quality Log (CSV)",
        data=df.to_csv(index=False),
        file_name="air_quality_log.csv",
        mime="text/csv"
    )

st.caption("Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
