import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="CPSFL Full Scorecard", layout="wide")

# Title and banner
st.title("🌟 CPSFL Scorecard Overview")
st.markdown("---")

# Load data
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRW3e5OB0urjbl6byFS2TkqUJGv7-xgb5kPBZUEKe3EyG9d5tML9MzBhVDLZzZAcBZAzPUZhReLbHR4/pub?output=csv"

try:
    df = pd.read_csv(url)

    # --- 1. SCORECARD SUMMARY ---
    st.subheader("📈 Scorecard Summary")
    summary = df.iloc[1:4, [0, 1, 2]].dropna()
    for _, row in summary.iterrows():
        st.markdown(f"**{row[0]} - {row[1]}**")
        st.markdown(f"*{row[2]}*")
    st.markdown("---")

    # --- 2. REPORTS COMPLIANCE BREAKDOWN ---
    st.subheader("📄 Required Reports Compliance Breakdown")
    reports = df.iloc[4:10, [0, 1]].dropna()
    st.dataframe(reports.rename(columns={0: "Description", 1: "Count"}), use_container_width=True)
    st.markdown("---")

    # --- 3. PERFORMANCE MEASURES ---
    st.subheader("📊 Overall Performance Measures")
    perf_df = pd.read_csv(url, skiprows=11, nrows=11, usecols=[0, 1, 2, 3])
    perf_df.columns = ['Measure ID', 'Description', 'Score', 'Target']
    perf_df.dropna(inplace=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    x = range(len(perf_df))
    ax.bar([i - 0.2 for i in x], perf_df['Score'], width=0.4, label='Score', color='green')
    ax.bar([i + 0.2 for i in x], perf_df['Target'], width=0.4, label='Target', color='gray')
    ax.set_xticks(x)
    ax.set_xticklabels(perf_df['Measure ID'], rotation=45, ha='right')
    ax.set_ylabel("Value")
    ax.set_title("Performance Measures: Score vs Target")
    ax.legend()
    st.pyplot(fig)
    st.markdown("---")

    # --- 4. WAITLIST COUNTS ---
    st.subheader("⏳ Open Cases by Waitlist Type")
    waitlist_df = pd.read_csv(url, skiprows=24, nrows=3, usecols=[0, 1])
    waitlist_df.columns = ['Description', 'Value']
    waitlist_df.dropna(inplace=True)
    st.dataframe(waitlist_df, use_container_width=True)
    st.markdown("---")

    # --- 5. AVERAGE DAYS ON WAITLIST ---
    st.subheader("📆 Average Days on Waitlist by Program")
    wait_days_df = pd.read_csv(url, skiprows=30, nrows=4, usecols=[0, 1])
    wait_days_df.columns = ['Program', 'Average Days']
    wait_days_df.dropna(inplace=True)
    st.dataframe(wait_days_df, use_container_width=True)
    st.markdown("---")

    # --- 6. CARISK COMPLETION SUMMARY ---
    st.subheader("📌 Carisk Completion Summary")
    completion_df = pd.read_csv(url, skiprows=37, nrows=5, usecols=[0, 1, 2])
    completion_df.columns = ['Description', 'Score', 'Detail']
    completion_df.dropna(inplace=True)
    for _, row in completion_df.iterrows():
        st.markdown(f"**{row['Description']} - {row['Score']}**")
        st.markdown(f"*{row['Detail']}*")

except Exception as e:
    st.error(f"Error loading data: {e}")
