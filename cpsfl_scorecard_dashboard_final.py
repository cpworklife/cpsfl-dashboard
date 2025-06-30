import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="CPSFL Scorecard Dashboard", layout="wide")

st.title("🌟 CPSFL Scorecard Dashboard")
st.markdown("Thriving Residents. Strong Communities.")

# Sheet setup
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

# SECTION 1 – Summary Metrics
st.header("📊 Summary Metrics")
try:
    summary_df = load_sheet(tabs["Summary Metrics"])
    st.dataframe(summary_df)
except Exception as e:
    st.error(f"Error loading Summary Metrics: {e}")

# SECTION 2 – Overall Score Breakdown
st.header("📈 Overall Score Breakdown")
try:
    overall_df = load_sheet(tabs["Overall Score Breakdown"])
    st.markdown("This score is the overall performance score for completed POMs (MHOs) and Discharges.")
    st.dataframe(overall_df)
except Exception as e:
    st.error(f"Error loading Overall Score Breakdown: {e}")

# SECTION 3 – Reports Compliance Breakdown
st.header("📄 Reports Compliance Breakdown")
try:
    reports_df = load_sheet(tabs["Reports Compliance Breakdown"])
    st.markdown("*Compliance is measured by computing the number of items submitted ON TIME divided by TOTAL items.*")
    st.dataframe(reports_df)
except Exception as e:
    st.error(f"Error loading Reports Compliance Breakdown: {e}")

# SECTION 4 – Performance Measure Breakdown
st.header("📊 Performance Measure Breakdown")
try:
    perf_df = load_sheet(tabs["Performance Measure Breakdown"])
    perf_df['Label'] = perf_df['Measure'] + "\n" + perf_df['Description']
    fig, ax = plt.subplots(figsize=(10, 6))
    x = range(len(perf_df))
    ax.bar([i - 0.2 for i in x], perf_df['Score'], width=0.4, label='Score', color='green')
    ax.bar([i + 0.2 for i in x], perf_df['Target'], width=0.4, label='Target', color='gray')
    ax.set_xticks(x)
    ax.set_xticklabels(perf_df['Label'], rotation=45, ha='right', fontsize=8)
    ax.set_ylabel("Value")
    ax.set_title("Performance Measures vs Targets")
    ax.legend()
    st.pyplot(fig)
except Exception as e:
    st.error(f"Error loading Performance Measure Breakdown: {e}")

# SECTION 5 – Waitlist Overview
st.header("⏳ Waitlist Overview")
try:
    waitlist_df = load_sheet(tabs["Waitlist Overview"])
    st.dataframe(waitlist_df)
except Exception as e:
    st.error(f"Error loading Waitlist Overview: {e}")

# SECTION 6 – Waitlist by Program
st.header("🏥 Waitlist by Program")
try:
    waitlist_prog_df = load_sheet(tabs["Waitlist by Program"])
    st.dataframe(waitlist_prog_df)
except Exception as e:
    st.error(f"Error loading Waitlist by Program: {e}")
