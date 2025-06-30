import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="CPSFL Scorecard Dashboard", layout="wide")

# Centered title
st.markdown("""
    <h1 style='text-align: center;'>CPSFL Scorecard Dashboard</h1>
    <h4 style='text-align: center;'>Thriving Residents. Strong Communities.</h4>
""", unsafe_allow_html=True)

# Google Sheet setup
base_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTVohW51_sRlF_mD7xijTJ8hW47jtIx2-9Ff2mNytnLKWTt926hR_yTtSihI7N2gu9EnEGP3wvjK43v/pub?gid={gid}&single=true&output=csv"
tabs = {
    "Summary Metrics": 965565385,
    "Overall Score Breakdown": 209468973,
    "Reports Compliance Breakdown": 467511660,
    "Performance Measure Breakdown": 401432916,
    "Waitlist Overview": 869606256,
    "Waitlist by Program": 1961299205
}

def load_sheet(gid):
    url = base_url.format(gid=gid)
    return pd.read_csv(url).reset_index(drop=True)

def draw_gauge(value, label):
    fig, ax = plt.subplots(figsize=(2.8, 1.5), subplot_kw={'projection': 'polar'})
    theta = np.linspace(0.0, np.pi, 100)
    radii = np.ones(100)
    ax.plot(theta, radii, color='white', lw=0)
    ax.bar(theta, radii, width=np.pi / 100, color='#00cc44')

    # White background for unfilled portion
    cutoff = int(value)
    ax.bar(theta[cutoff:], radii[cutoff:], width=np.pi / 100, color='lightgray')

    # Remove grid and axis
    ax.set_axis_off()
    ax.set_ylim(0, 1.1)

    # Add the value in center
    ax.text(0, -0.3, f"{value:.2f}", fontsize=16, ha='center', va='center', fontweight='bold')
    ax.text(0, -0.55, "%", fontsize=10, ha='center', va='center')
    ax.set_title(label, va='bottom', fontsize=10)
    return fig

# SECTION 1 – Summary Metrics
st.header("\U0001F4CA Summary Metrics")
try:
    summary_df = load_sheet(tabs["Summary Metrics"])
    
    # Check if 'Description' column is present
    required_cols = ["Description", "Score", "Detailed Description"]
    missing_cols = [col for col in required_cols if col not in summary_df.columns]
    
    if missing_cols:
        st.error(f"Missing columns in Summary Metrics: {missing_cols}")
        st.write("Available columns:", summary_df.columns.tolist())
    else:
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
except Exception as e:
    st.error(f"Error loading Summary Metrics: {e}")


# SECTION 2 – Overall Score Breakdown
st.header("📈 Overall Score Breakdown")
try:
    overall_df = load_sheet(tabs["Overall Score Breakdown"])
    st.markdown("This score is the overall performance score for completed POMs (MHOs) and Discharges.")
    st.dataframe(overall_df, use_container_width=True, hide_index=True)
except Exception as e:
    st.error(f"Error loading Overall Score Breakdown: {e}")

# SECTION 3 – Reports Compliance Breakdown
st.header("📄 Reports Compliance Breakdown")
try:
    reports_df = load_sheet(tabs["Reports Compliance Breakdown"])
    st.markdown("*Compliance is measured by computing the number of items submitted ON TIME divided by TOTAL items.*")
    st.dataframe(reports_df, use_container_width=True, hide_index=True)
except Exception as e:
    st.error(f"Error loading Reports Compliance Breakdown: {e}")

# SECTION 4 – Performance Measure Breakdown
st.header("📊 Performance Measure Breakdown")
try:
    perf_df = load_sheet(tabs["Performance Measure Breakdown"])
    st.dataframe(perf_df, use_container_width=True, hide_index=True)
except Exception as e:
    st.error(f"Error loading Performance Measure Breakdown: {e}")

# SECTION 5 – Waitlist Overview
st.header("⏳ Waitlist Overview")
try:
    waitlist_df = load_sheet(tabs["Waitlist Overview"])
    st.dataframe(waitlist_df, use_container_width=True, hide_index=True)
except Exception as e:
    st.error(f"Error loading Waitlist Overview: {e}")

# SECTION 6 – Waitlist by Program
st.header("🏥 Waitlist by Program")
try:
    waitlist_prog_df = load_sheet(tabs["Waitlist by Program"])
    st.dataframe(waitlist_prog_df, use_container_width=True, hide_index=True)
except Exception as e:
    st.error(f"Error loading Waitlist by Program: {e}")
