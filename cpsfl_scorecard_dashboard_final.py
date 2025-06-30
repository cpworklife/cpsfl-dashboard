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
    df.columns = df.columns.str.strip()  # Clean up column names
    return df.reset_index(drop=True)

def half_circle_gauge(value, label):
    fig, ax = plt.subplots(figsize=(3, 2), subplot_kw={'projection': 'polar'})
    theta = np.linspace(np.pi, 2 * np.pi, 100)
    ax.plot(theta, [1]*100, color='lightgray', linewidth=20)
    filled = int(value)
    ax.plot(theta[:filled], [1]*filled, color='green', linewidth=20)
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.set_title(f"{label}\n{value}%", fontsize=10)
    ax.set_facecolor("white")
    ax.grid(False)
    ax.set_theta_zero_location("W")
    ax.set_theta_direction(-1)
    ax.set_rlim(0, 1.1)
    return fig

# SECTION 1 – Summary Metrics
st.header("📊 Summary Metrics")
try:
    summary_df = load_sheet(tabs["Summary Metrics"])

     # Clean Score column (remove % and convert to float)
    summary_df["Score"] = summary_df["Score"].str.replace("%", "").astype(float)

    # Half-circle gauges
    col1, col2, col3 = st.columns(3)
    with col1:
        score1 = summary_df.loc[0, "Score"]
        st.pyplot(half_circle_gauge(score1, summary_df.loc[0, "Description"]))
    with col2:
        score2 = summary_df.loc[1, "Score"]
        st.pyplot(half_circle_gauge(score2, summary_df.loc[1, "Description"]))
    with col3:
        score3 = summary_df.loc[2, "Score"]
        st.pyplot(half_circle_gauge(score3, summary_df.loc[2, "Description"]))


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
