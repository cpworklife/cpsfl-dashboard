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
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df.reset_index(drop=True)

def half_circle_gauge(value, label):
    fig, ax = plt.subplots(figsize=(3.5, 2.2), subplot_kw={'projection': 'polar'})

    # Background: full half-circle in light gray
    theta = np.linspace(np.pi, 2 * np.pi, 100)
    ax.bar(theta, [1]*len(theta), width=np.pi/100, color='lightgray', bottom=0.5)

    # Foreground: green progress bar filling left to right
    filled_theta = np.linspace(np.pi, np.pi + (value / 100.0) * np.pi, 100)
    ax.bar(filled_theta, [1]*len(filled_theta), width=np.pi/100, color='green', bottom=0.5)

    # Hide axis ticks and grid
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.grid(False)

    # Positioning for correct fill direction and upright
    ax.set_theta_zero_location("W")
    ax.set_theta_direction(-1)
    ax.set_rlim(0, 1.5)

    # Label above gauge
    ax.set_title(label, va='bottom', fontsize=11)

    # Center text (value)
    ax.text(0, 0, f"{value:.2f}%", fontsize=14, fontweight='bold', ha='center', va='center')

    # Add 0 and 100 on either side below the arc
    ax.text(np.pi, 0.25, "0", ha='center', va='center', fontsize=8)
    ax.text(2*np.pi, 0.25, "100", ha='center', va='center', fontsize=8)

    return fig


# SECTION 1 – Summary Metrics
st.header("📊 Summary Metrics")
try:
    summary_df = load_sheet(tabs["Summary Metrics"])
    summary_df["Score"] = summary_df["Score"].str.replace("%", "").astype(float)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.pyplot(half_circle_gauge(summary_df.loc[0, "Score"], summary_df.loc[0, "Description"]))
    with col2:
        st.pyplot(half_circle_gauge(summary_df.loc[1, "Score"], summary_df.loc[1, "Description"]))
    with col3:
        st.pyplot(half_circle_gauge(summary_df.loc[2, "Score"], summary_df.loc[2, "Description"]))

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
