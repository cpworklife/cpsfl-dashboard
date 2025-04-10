import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="CPSFL Scorecard Dashboard", layout="wide")
st.title("📊 CPSFL Scorecard Dashboard")

uploaded_file = st.file_uploader("Upload your Scorecard Excel file", type=["xlsx"])

if uploaded_file:
    try:
        # Read the uploaded Excel file
        excel_file = pd.ExcelFile(uploaded_file)
        sheet_names = excel_file.sheet_names

        if 'Data Input' not in sheet_names:
            st.error("Couldn't find a 'Data Input' sheet in the Excel file.")
        else:
            df = excel_file.parse('Data Input')
            df = df.dropna(subset=['Date',
                                   'Overall % Completed (MHOs & Discharges)',
                                   'Required Reports Compliance',
                                   'Overall Performance Measure',
                                   'Missing records',
                                   'Total Possible'])
            df['Date'] = pd.to_datetime(df['Date'])

            # Format dates to month/day
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
        st.error(f"An error occurred: {e}")
else:
    st.info("👆 Upload an Excel file to get started!")
