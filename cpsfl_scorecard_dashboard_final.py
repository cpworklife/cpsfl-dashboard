import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import numpy as np

st.set_page_config(page_title="CPSFL Scorecard Dashboard", layout="wide")

# Scrolling banner
st.markdown(
    """
    <marquee style='font-size:24px; color:#00796B; background:#E0F7FA; padding:10px;'>
    🌟 Community Partners of South Florida 🌟
    </marquee>
    """,
    unsafe_allow_html=True
)

# Dark mode toggle (simulated with background color swap)
dark_mode = st.toggle("🌙 Dark Mode")
if dark_mode:
    st.markdown("""
    <style>
        body { background-color: #121212; color: white; }
        .stApp { background-color: #121212; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 CPSFL Scorecard Dashboard")

# Refresh button
if st.button("🔄 Refresh Data"):
    st.rerun()

# You will need to define your sheet URLs here:
sheet_url = "YOUR_FIRST_GOOGLE_SHEET_URL"
performance_sheet_url = "YOUR_PERFORMANCE_SHEET_URL"

# Dummy gauge plot function (replace with your actual gauge function)
def plot_gauge(title, value):
    fig, ax = plt.subplots()
    ax.barh([0], [value], color='green')
    ax.set_xlim(0, 100)
    ax.set_yticks([])
    ax.set_title(f"{title}: {value:.1f}%")
    return fig

try:
    df = pd.read_csv(sheet_url)
    df['Date'] = pd.to_datetime(df['Date'].astype(str), errors='coerce')
    df = df.dropna(subset=['Date'])
    df['DateLabel'] = df['Date'].dt.strftime('%-m/%-d')
    perf_df = pd.read_csv(performance_sheet_url)

    latest_overall_score = df['Overall % Completed (MHOs & Discharges)'].iloc[-1]
    latest_reports_compliance = df['Required Reports Compliance'].iloc[-1]
    sheet1_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRW3e5OB0urjbl6byFS2Tk_
