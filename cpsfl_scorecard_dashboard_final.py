import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="CPSFL One-Page Scorecard", layout="wide")

# Google Sheet URL
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTVohW51_sRlF_mD7xijTJ8hW47jtIx2-9Ff2mNytnLKWTt926hR_yTtSihI7N2gu9EnEGP3wvjK43v/pub?gid=0&single=true&output=csv"

# Load the data
try:
    df = pd.read_csv(sheet_url)

    st.title("🌟 Community Partners of South Florida - Scorecard Dashboard")

    # Section 1: Overall Metrics
    st.header("📈 Overview Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Overall % Completed", f"{df['Overall Score'].dropna().iloc[-1]}%")
    col2.metric("Reports Compliance", f"{df['Reports Compliance'].dropna().iloc[-1]}%")
    col3.metric("Performance Measure", f"{df['Performance Measure'].dropna().iloc[-1]}%")

    st.markdown("---")

    # Section 2: Record Totals
    st.header("📊 Record Totals")
    st.write(f"**Total Possible Records:** {int(df['Total Possible Records'].dropna().iloc[-1])}")
    st.write(f"**Total Completed Records:** {int(df['Actual Records'].dropna().iloc[-1])}")
    st.write(f"**Total Missing Records:** {int(df['Missing Records'].dropna().iloc[-1])}")

    st.markdown("---")

    # Section 3: Reports Breakdown
    st.header("📄 Reports Compliance Breakdown")
    st.write(f"**On Time Reports:** {int(df['On Time Reports'].dropna().iloc[-1])}")
    st.write(f"**Late Reports:** {int(df['Late Reports'].dropna().iloc[-1])}")
    st.write(f"**Missing Reports:** {int(df['Missing Reports'].dropna().iloc[-1])}")
    st.write(f"**Rejected Reports:** {int(df['Rejected Reports'].dropna().iloc[-1])}")
    st.write(f"**Pending Review:** {int(df['Pending Review'].dropna().iloc[-1])}")
    st.write(f"**Total Reports:** {int(df['Total Reports'].dropna().iloc[-1])}")

    st.markdown("---")

    # Section 4: Performance Measures
    st.header("📌 Performance Measure Details")
    measures = df.filter(regex="M0[0-9]+|M07[0-9]+").dropna(how='all', axis=1)
    for col in measures.columns:
        score_col = f"{col} Score"
        target_col = f"{col} Target"
        if score_col in df.columns and target_col in df.columns:
            st.write(f"**{col}**")
            st.progress(min(df[score_col].dropna().iloc[-1] / df[target_col].dropna().iloc[-1], 1.0))
            st.caption(f"Score: {df[score_col].dropna().iloc[-1]} | Target: {df[target_col].dropna().iloc[-1]}")

    st.markdown("---")

    # Section 5: Waitlist Information
    st.header("🕒 Carisk Waitlist Snapshot")
    st.write(f"**Outpatient Cases:** {int(df['Outpatient Waitlist Cases'].dropna().iloc[-1])}")
    st.write(f"**Wrap Around Cases:** {int(df['Wrap Around Waitlist Cases'].dropna().iloc[-1])}")
    st.write(f"**Total Open Cases:** {int(df['Total Open Cases'].dropna().iloc[-1])}")

    st.markdown("### Average Days by Program")
    programs = ['CMH', 'AMH', 'ASA', 'ASA & AMH']
    for program in programs:
        st.write(f"**{program}:** {int(df[program].dropna().iloc[-1])} days")

except Exception as e:
    st.error(f"An error occurred while loading the Google Sheet: {e}")
