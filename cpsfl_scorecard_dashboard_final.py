import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="CPSFL Scorecard Dashboard", layout="wide")

# Banner
st.markdown(
    """
    <marquee style='font-size:24px; color:#00796B; background:#E0F7FA; padding:10px;'>
    🌟 Community Partners of South Florida - Scorecard Dashboard 🌟
    </marquee>
    """,
    unsafe_allow_html=True
)

# Sheet base URL and GIDs for each tab
base_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTVohW51_sRlF_mD7xijTJ8hW47jtIx2-9Ff2mNytnLKWTt926hR_yTtSihI7N2gu9EnEGP3wvjK43v/pub?gid={gid}&single=true&output=csv"

tabs = {
    "Summary Metrics": "0",
    "Overall Score Breakdown": "1137431240",
    "Reports Compliance Breakdown": "2072559720",
    "Performance Measure Breakdown": "460550068",
    "Waitlist Overview": "963423245",
    "Waitlist by Program": "1204475949"
}

def load_data(gid):
    url = base_url.format(gid=gid)
    return pd.read_csv(url)

# 1. Summary Metrics
st.header("📋 Summary Metrics")
try:
    df_summary = load_data(tabs["Summary Metrics"])
    st.dataframe(df_summary, use_container_width=True)
except Exception as e:
    st.error(f"Error loading Summary Metrics: {e}")

# 2. Overall Score Breakdown
st.header("📈 Overall Score Breakdown")
try:
    df_overall = load_data(tabs["Overall Score Breakdown"])
    st.dataframe(df_overall, use_container_width=True)
except Exception as e:
    st.error(f"Error loading Overall Score Breakdown: {e}")

# 3. Reports Compliance Breakdown
st.header("📄 Reports Compliance Breakdown")
try:
    df_reports = load_data(tabs["Reports Compliance Breakdown"])
    st.dataframe(df_reports, use_container_width=True)
except Exception as e:
    st.error(f"Error loading Reports Compliance Breakdown: {e}")

# 4. Performance Measure Breakdown
st.header("📊 Performance Measure Breakdown")
try:
    df_perf = load_data(tabs["Performance Measure Breakdown"])
    df_perf['Label'] = df_perf['Measure'] + "\n" + df_perf['Description']
    fig, ax = plt.subplots(figsize=(10, 6))
    x = range(len(df_perf))
    ax.bar([i - 0.2 for i in x], df_perf['Score'], width=0.4, label='Score', color='green')
    ax.bar([i + 0.2 for i in x], df_perf['Target'], width=0.4, label='Target', color='gray')
    ax.set_xticks(x)
    ax.set_xticklabels(df_perf['Label'], rotation=0, ha='center', fontsize=7)
    ax.set_ylabel("Percentage")
    ax.set_title("Performance Measure Score vs Target")
    ax.legend()
    st.pyplot(fig)
    st.dataframe(df_perf.drop(columns=["Label"]), use_container_width=True)
except Exception as e:
    st.error(f"Error loading Performance Measure Breakdown: {e}")

# 5. Waitlist Overview
st.header("📌 Waitlist Overview")
try:
    df_waitlist = load_data(tabs["Waitlist Overview"])
    st.dataframe(df_waitlist, use_container_width=True)
except Exception as e:
    st.error(f"Error loading Waitlist Overview: {e}")

# 6. Waitlist by Program
st.header("📌 Waitlist by Program")
try:
    df_program = load_data(tabs["Waitlist by Program"])
    st.dataframe(df_program, use_container_width=True)
except Exception as e:
    st.error(f"Error loading Waitlist by Program: {e}")
