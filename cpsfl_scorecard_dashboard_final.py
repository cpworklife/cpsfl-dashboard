import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="CPSFL Scorecard Dashboard", layout="wide")

# Scrolling banner
st.markdown(
    """
    <marquee style='font-size:24px; color:#00796B; background:#E0F7FA; padding:10px;'>
    🌟 Community Partners of South Florida 🌟
    </marquee>
    """,
    unsafe_allow_html=True
)

# Dark mode toggle
if st.toggle("🌙 Dark Mode"):
    st.markdown("""
    <style>
        body { background-color: #121212; color: white; }
        .stApp { background-color: #121212; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 CPSFL Scorecard Dashboard")

if st.button("🔄 Refresh Data"):
    st.rerun()

# Sheet URLs
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTVohW51_sRlF_mD7xijTJ8hW47jtIx2-9Ff2mNytnLKWTt926hR_yTtSihI7N2gu9EnEGP3wvjK43v/pub?gid=0&single=true&output=csv"
performance_sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTVohW51_sRlF_mD7xijTJ8hW47jtIx2-9Ff2mNytnLKWTt926hR_yTtSihI7N2gu9EnEGP3wvjK43v/pub?gid=460550068&single=true&output=csv"

try:
    df = pd.read_csv(sheet_url)
    df['Date'] = pd.to_datetime(df['Date'].astype(str), errors='coerce')
    df = df.dropna(subset=['Date'])
    df['DateLabel'] = df['Date'].dt.strftime('%-m/%-d')
    perf_df = pd.read_csv(performance_sheet_url)

    # Metric values
    latest_overall_score = df.iloc[-1]['Overall % Completed (MHOs & Discharges)']
    latest_reports_compliance = df.iloc[-1]['Required Reports Compliance']
    overall_perf_measure = df.iloc[-1]['Overall Performance Measure']

    tab1, tab2 = st.tabs(["📋 Scorecard Breakdown", "📊 Visual Dashboard"])

    with tab1:
        st.header("📈 Overall Score - {:.2f}%".format(latest_overall_score))
        st.markdown("This score is the overall performance score for completed POMs (MHOs) and Discharges. This score also includes POMs that have been submitted late or are missing.")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Possible Records", df.iloc[-1]['Total Possible'])
        col2.metric("Actual Records", df.iloc[-1]['Total Records Completed'])
        col3.metric("Records Missing", df.iloc[-1]['Missing records'])

        st.divider()
        st.header("📈 Required Reports Compliance - {:.0f}%".format(latest_reports_compliance))
        st.markdown("""
        *Required Contractual Reports Compliance is measured by computing the number of items submitted ON TIME divided by TOTAL items.*
        """)
        rpt_cols = st.columns(3)
        rpt_cols[0].metric("On Time Reports", int(df.iloc[-1]['On Time']))
        rpt_cols[1].metric("Late Reports", int(df.iloc[-1]['Late']))
        rpt_cols[2].metric("Missing/Overdue", int(df.iloc[-1]['Missing']))
        rpt_cols = st.columns(3)
        rpt_cols[0].metric("Rejected Reports", int(df.iloc[-1]['Rejected']))
        rpt_cols[1].metric("Pending Review", int(df.iloc[-1]['Pending Review']))
        rpt_cols[2].metric("Total Reports", int(df.iloc[-1]['Total Reports']))

        st.divider()
        st.header("📈 Overall Performance Measure - {:.0f}%".format(overall_perf_measure))
        st.markdown("This score is comprised of 10 measures below. Each has a target shown alongside the current score.")

        perf_df['Label'] = perf_df['Measure'] + "\n" + perf_df['Description']
        fig, ax = plt.subplots(figsize=(10, 6))
        x = range(len(perf_df))
        ax.bar([i - 0.2 for i in x], perf_df['Score'], width=0.4, label='Score', color='green')
        ax.bar([i + 0.2 for i in x], perf_df['Target'], width=0.4, label='Target', color='gray')
        ax.set_xticks(x)
        ax.set_xticklabels(perf_df['Label'], rotation=0, fontsize=8, wrap=True)
        ax.set_ylabel("Value")
        ax.set_title("Performance Measures")
        ax.legend()
        st.pyplot(fig)

    with tab2:
        st.subheader("📈 Overall Score YTD")
        fig1, ax1 = plt.subplots()
        ax1.plot(df['DateLabel'], df['Overall % Completed (MHOs & Discharges)'], marker='o', color='green')
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Overall Score")
        ax1.set_title("Overall Score Trend YTD")
        ax1.grid(True)
        plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')
        st.pyplot(fig1)

        st.subheader("✅ Completed Records YTD")
        completed = df['Total Possible'] - df['Missing records']
        fig2, ax2 = plt.subplots()
        ax2.plot(df['DateLabel'], completed, marker='o', color='green')
        ax2.set_title("Completed Records YTD")
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Count")
        ax2.grid(True)
        plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
        st.pyplot(fig2)

        st.subheader("❌ Missing Records")
        fig3, ax3 = plt.subplots()
        ax3.plot(df['DateLabel'], df['Missing records'], marker='s', color='green')
        ax3.set_title("Missing Records YTD")
        ax3.set_xlabel("Date")
        ax3.set_ylabel("Count")
        ax3.grid(True)
        plt.setp(ax3.get_xticklabels(), rotation=45, ha='right')
        st.pyplot(fig3)

        st.subheader("📄 Required Reports Compliance")
        fig4, ax4 = plt.subplots()
        ax4.plot(df['DateLabel'], df['Required Reports Compliance'], marker='o', color='green')
        ax4.set_xlabel("Date")
        ax4.set_ylabel("Compliance %")
        ax4.set_title("Contractual Reports Compliance Over Time")
        ax4.grid(True)
        plt.setp(ax4.get_xticklabels(), rotation=45, ha='right')
        st.pyplot(fig4)

        with st.expander("🔍 View Raw Data"):
            st.dataframe(df)

except Exception as e:
    st.error(f"An error occurred while loading the Google Sheet: {e}")
