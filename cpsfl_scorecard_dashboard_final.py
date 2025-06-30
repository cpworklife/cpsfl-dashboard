import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="CPSFL Scorecard Dashboard", layout="wide")

# Centered title and subtitle
st.markdown("<h1 style='text-align: center;'>CPSFL Scorecard Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Thriving Residents. Strong Communities.</h4>", unsafe_allow_html=True)

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
    return pd.read_csv(url)

def draw_half_circle_gauge(value, title):
    fig, ax = plt.subplots(figsize=(3, 2))
    ax.axis("off")
    theta = np.linspace(-np.pi, 0, 100)
    r = 1
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    ax.plot(x, y, color="gray", linewidth=20, alpha=0.1)
    fill = int(value)
    fill_theta = np.linspace(-np.pi, -np.pi + (fill / 100) * np.pi, 100)
    x_fill = r * np.cos(fill_theta)
    y_fill = r * np.sin(fill_theta)
    ax.plot(x_fill, y_fill, color="green", linewidth=20)
    ax.text(0, -0.1, f"{value:.2f}", ha="center", va="center", fontsize=16, fontweight="bold")
    ax.text(0, -0.3, "%", ha="center", va="center", fontsize=12)
    ax.set_title(title, fontsize=12)
    return fig

# SECTION 1 – Summary Metrics
st.header("📊 Summary Metrics")
try:
    summary_df = load_sheet(tabs["Summary Metrics"])

    # Extract values for gauges
    overall_score = float(summary_df.loc[summary_df['Description'] == "Overall Score", 'Score'].values[0])
    compliance_score = float(summary_df.loc[summary_df['Description'] == "Required Reports Compliance", 'Score'].values[0])
    perf_score = float(summary_df.loc[summary_df['Description'] == "Overall Performance Measure", 'Score'].values[0])

    # Display gauges
    col1, col2, col3 = st.columns(3)
    with col1:
        st.pyplot(draw_half_circle_gauge(overall_score, "Overall % Completed"))
    with col2:
        st.pyplot(draw_half_circle_gauge(compliance_score, "Required Reports Compliance"))
    with col3:
        st.pyplot(draw_half_circle_gauge(perf_score, "Overall Performance Measure"))

    # Display the rest of the summary table
    st.dataframe(summary_df, hide_index=True)

except Exception as e:
    st.error(f"Error loading Summary Metrics: {e}")

# --- Remaining sections stay unchanged ---

# SECTION 2 – Overall Score Breakdown
st.header("📈 Overall Score Breakdown")
try:
    overall_df = load_sheet(tabs["Overall Score Breakdown"])
    st.markdown("This score is the overall performance score for completed POMs (MHOs) and Discharges.")
    st.dataframe(overall_df, hide_index=True)
except Exception as e:
    st.error(f"Error loading Overall Score Breakdown: {e}")

# SECTION 3 – Reports Compliance Breakdown
st.header("📄 Reports Compliance Breakdown")
try:
    reports_df = load_sheet(tabs["Reports Compliance Breakdown"])
    st.markdown("*Compliance is measured by computing the number of items submitted ON TIME divided by TOTAL items.*")
    st.dataframe(reports_df, hide_index=True)
except Exception as e:
    st.error(f"Error loading Reports Compliance Breakdown: {e}")

# SECTION 4 – Performance Measure Breakdown
st.header("📊 Performance Measure Breakdown")
try:
    perf_df = load_sheet(tabs["Performance Measure Breakdown"])
    st.dataframe(perf_df, hide_index=True)
except Exception as e:
    st.error(f"Error loading Performance Measure Breakdown: {e}")

# SECTION 5 – Waitlist Overview
st.header("⏳ Waitlist Overview")
try:
    waitlist_df = load_sheet(tabs["Waitlist Overview"])
    st.dataframe(waitlist_df, hide_index=True)
except Exception as e:
    st.error(f"Error loading Waitlist Overview: {e}")

# SECTION 6 – Waitlist by Program
st.header("🏥 Waitlist by Program")
try:
    waitlist_prog_df = load_sheet(tabs["Waitlist by Program"])
    st.dataframe(waitlist_prog_df, hide_index=True)
except Exception as e:
    st.error(f"Error loading Waitlist by Program: {e}")
