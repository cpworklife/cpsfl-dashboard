import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="CPSFL Scorecard Dashboard", layout="wide")

st.title("🌟 CPSFL Scorecard Dashboard")

# Google Sheet ID and GID mappings
sheet_id = "1zb199yRXke-kYHDBtAXAhkmdlbYlldwYaeLehVV46qk"
tabs = {
    "Summary Metrics": "965565385",
    "Overall Score Breakdown": "209468973",
    "Reports Compliance Breakdown": "467511660",
    "Performance Measure Breakdown": "401432916",
    "Waitlist Overview": "869606256",
    "Waitlist by Program": "1961299205"
}

# Helper to load a sheet
def load_sheet(gid):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    return pd.read_csv(url)

try:
    # Load each sheet
    summary_df = load_sheet(tabs["Summary Metrics"])
    overall_score_df = load_sheet(tabs["Overall Score Breakdown"])
    reports_df = load_sheet(tabs["Reports Compliance Breakdown"])
    performance_df = load_sheet(tabs["Performance Measure Breakdown"])
    waitlist_overview_df = load_sheet(tabs["Waitlist Overview"])
    waitlist_by_program_df = load_sheet(tabs["Waitlist by Program"])

    # --- Summary Metrics ---
    st.header("📈 Summary Metrics")
    st.dataframe(summary_df)

    # --- Overall Score Breakdown ---
    st.header("📊 Overall Score Breakdown")
    st.dataframe(overall_score_df)

    # --- Reports Compliance Breakdown ---
    st.header("📝 Reports Compliance Breakdown")
    st.dataframe(reports_df)

    # --- Performance Measure Breakdown ---
    st.header("🎯 Performance Measure Breakdown")
    st.dataframe(performance_df)

    # Optional: Plot Performance Score vs Target
    if 'Score' in performance_df.columns and 'Target' in performance_df.columns:
        st.subheader("📈 Performance Score vs Target")
        fig, ax = plt.subplots(figsize=(10, 6))
        x = range(len(performance_df))
        ax.bar([i - 0.2 for i in x], performance_df['Score'], width=0.4, label='Score', color='green')
        ax.bar([i + 0.2 for i in x], performance_df['Target'], width=0.4, label='Target', color='gray')
        ax.set_xticks(x)
        ax.set_xticklabels(performance_df['Measure'], rotation=45, ha='right', fontsize=8)
        ax.set_ylabel("Value")
        ax.set_title("Performance Score vs Target")
        ax.legend()
        st.pyplot(fig)

    # --- Waitlist Overview ---
    st.header("📋 Waitlist Overview")
    st.dataframe(waitlist_overview_df)

    # --- Waitlist by Program ---
    st.header("🏥 Waitlist by Program")
    st.dataframe(waitlist_by_program_df)

except Exception as e:
    st.error(f"Error loading data: {e}")
