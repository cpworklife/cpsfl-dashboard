import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="CPSFL Scorecard Dashboard", layout="wide")
st.title("📊 CPSFL Scorecard Dashboard")

# Load data directly from Google Sheets CSV link
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTVohW51_sRlF_mD7xijTJ8hW47jtIx2-9Ff2mNytnLKWTt926hR_yTtSihI7N2gu9EnEGP3wvjK43v/pub?output=csv"

# Refresh button
if st.button("🔄 Refresh Data"):
    st.experimental_rerun()

try:
    df = pd.read_csv(sheet_url)
    df['Date'] = pd.to_datetime(df['Date'])
    df['DateLabel'] = df['Date'].dt.strftime('%-m/%-d')

    # Line Chart: Overall Score
    st.subheader("📈 Overall Score Over Time")
    fig1, ax1 = plt.subplots()
    ax1.plot(df['DateLabel'], df['Overall % Completed (MHOs & Discharges)'], marker='o', color='green')
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Overall Score")
    ax1.set_title("Overall Score Trend")
    ax1.grid(True)
    plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig1)

    # Stacked Area Chart: Completed vs Missing
    st.subheader("📊 Completed vs Missing Records")
    completed = df['Total Possible'] - df['Missing records']
    missing = df['Missing records']
    fig2, ax2 = plt.subplots()
    ax2.stackplot(df['DateLabel'], completed, missing, labels=['Completed', 'Missing'])
    ax2.set_title("MHOs/Discharges Over Time")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Record Count")
    ax2.legend(loc='upper left')
    ax2.grid(True)
    plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig2)

    # Combo Chart
    st.subheader("📉 Scorecard Metrics Over Time")
    fig3, ax3 = plt.subplots()
    ax3.plot(df['DateLabel'], df['Overall % Completed (MHOs & Discharges)'], label='Overall Score Trend', marker='o', color='green')
    ax3.plot(df['DateLabel'], df['Required Reports Compliance'], label='MHO Discharges Over Time', marker='s')
    ax3.set_ylim(0, 105)
    ax3.set_title("Key Metrics Comparison")
    ax3.set_xlabel("Date")
    ax3.set_ylabel("%")
    ax3.legend()
    ax3.grid(True)
    plt.setp(ax3.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig3)

    # Optional: Data preview
    with st.expander("🔍 View Raw Data"):
        st.dataframe(df)

except Exception as e:
    st.error(f"An error occurred while loading the Google Sheet: {e}")
