
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

# Dark mode toggle
dark_mode = st.toggle("🌙 Dark Mode")
if dark_mode:
    st.markdown("""
    <style>
        body { background-color: #121212; color: white; }
        .stApp { background-color: #121212; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 CPSFL Scorecard Dashboard")

# Gauge-style Overview
def plot_gauge(title, value):
    fig, ax = plt.subplots(figsize=(4, 2.5))
    theta = np.linspace(0, np.pi, 100)
    x = np.cos(theta)
    y = np.sin(theta)
    ax.plot(x, y, color='lightgray', linewidth=20)

    end_angle = (value / 100.0) * np.pi
    filled_theta = np.linspace(0, end_angle, 100)
    fx = np.cos(filled_theta)
    fy = np.sin(filled_theta)
    ax.plot(fx, fy, color='green', linewidth=20)

    ax.text(0, -0.3, f"{value:.2f}%", ha='center', va='center', fontsize=18, fontweight='bold')
    ax.set_title(title, fontsize=14)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig

# Data source URLs
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTVohW51_sRlF_mD7xijTJ8hW47jtIx2-9Ff2mNytnLKWTt926hR_yTtSihI7N2gu9EnEGP3wvjK43v/pub?output=csv"
performance_sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTVohW51_sRlF_mD7xijTJ8hW47jtIx2-9Ff2mNytnLKWTt926hR_yTtSihI7N2gu9EnEGP3wvjK43v/pub?gid=460550068&single=true&output=csv"
sheet1_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTVohW51_sRlF_mD7xijTJ8hW47jtIx2-9Ff2mNytnLKWTt926hR_yTtSihI7N2gu9EnEGP3wvjK43v/pub?output=csv"

# Refresh button
if st.button("🔄 Refresh Data"):
    st.rerun()

try:
    df = pd.read_csv(sheet_url)
    df['Date'] = pd.to_datetime(df['Date'].astype(str), errors='coerce')
    df = df.dropna(subset=['Date'])
    df['DateLabel'] = df['Date'].dt.strftime('%-m/%-d')
    perf_df = pd.read_csv(performance_sheet_url)
    overall_perf_measure = pd.read_csv(sheet1_url)['Score'].dropna().iloc[-1]

    latest_overall_score = df['Overall % Completed (MHOs & Discharges)'].iloc[-1]
    latest_reports_compliance = df['Required Reports Compliance'].iloc[-1]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.pyplot(plot_gauge("Overall % Completed", latest_overall_score))
    with col2:
        st.pyplot(plot_gauge("Required Reports Compliance", latest_reports_compliance))
    with col3:
        st.pyplot(plot_gauge("Overall Performance Measure", overall_perf_measure))

except Exception as e:
    st.error(f"An error occurred while loading the Google Sheet: {e}")
