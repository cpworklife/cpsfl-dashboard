import streamlit as st
import pandas as pd

# Google Sheet URLs with GIDs
sheet_id = "1zb199yRXke-kYHDBtAXAhkmdlbYlldwYaeLehVV46qk"
tabs = {
    "Summary Metrics": 965565385,
    "Overall Score Breakdown": 209468973,
    "Reports Compliance Breakdown": 467511660,
    "Performance Measure Breakdown": 401432916,
    "Waitlist Overview": 869606256,
    "Waitlist by Program": 1961299205,
}

# Function to load each sheet
def load_sheet(gid):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    return pd.read_csv(url)

# Load dataframes
summary_df = load_sheet(tabs["Summary Metrics"])
overall_df = load_sheet(tabs["Overall Score Breakdown"])
compliance_df = load_sheet(tabs["Reports Compliance Breakdown"])
performance_df = load_sheet(tabs["Performance Measure Breakdown"])
waitlist_df = load_sheet(tabs["Waitlist Overview"])
program_df = load_sheet(tabs["Waitlist by Program"])

# Dashboard layout
st.set_page_config(page_title="CPSFL Scorecard Dashboard", layout="wide")
st.title("📊 CPSFL Scorecard Dashboard")

# --- Summary Metrics ---
st.header("📈 Summary Metrics")
for i, row in summary_df.iterrows():
    st.metric(label=row["Description"], value=row["Score"])
    if pd.notna(row.get("Detailed Description")):
        st.caption(row["Detailed Description"])

# --- Overall Score Breakdown ---
st.header("📉 Overall Score Breakdown")
st.dataframe(overall_df, use_container_width=True)

# --- Reports Compliance Breakdown ---
st.header("📋 Reports Compliance Breakdown")
st.dataframe(compliance_df, use_container_width=True)

# --- Performance Measure Breakdown ---
st.header("📊 Performance Measure Breakdown")
st.dataframe(performance_df, use_container_width=True)

# --- Waitlist Overview ---
st.header("📌 Waitlist Overview")
st.dataframe(waitlist_df, use_container_width=True)

# --- Waitlist by Program ---
st.header("📌 Waitlist by Program")
st.dataframe(program_df, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Updated automatically from live Google Sheets.")
