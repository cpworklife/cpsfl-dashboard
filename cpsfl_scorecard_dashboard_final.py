
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
dark_mode = st.toggle("🌙 Dark Mode")
if dark_mode:
    st.markdown("""
    <style>
        body { background-color: #121212; color: white; }
        .stApp { background-color: #121212; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 CPSFL Scorecard Dashboard")

# Refresh button
if st.button("🔄 Refresh Data"):
    st.rerun()

# Google Sheet URLs
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTVohW51_sRlF_mD7xijTJ8hW47jtIx2-9Ff2mNytnLKWTt926hR_yTtSihI7N2gu9EnEGP3wvjK43v/pub?gid=0&single=true&output=csv"
performance_sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTVohW51_sRlF_mD7xijTJ8hW47jtIx2-9Ff2mNytnLKWTt926hR_yTtSihI7N2gu9EnEGP3wvjK43v/pub?gid=460550068&single=true&output=csv"

# ✅ Load progress bar values BEFORE the try block
sheet1_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTVohW51_sRlF_mD7xijTJ8hW47jtIx2-9Ff2mNytnLKWTt926hR_yTtSihI7N2gu9EnEGP3wvjK43v/pub?output=csv"
sheet1_df = pd.read_csv(sheet1_url)
overall_completed = sheet1_df.iloc[-1, 1]
required_compliance = sheet1_df.iloc[-1, 2]
overall_performance = sheet1_df.iloc[-1, 3]

st.subheader("📌 Key Metrics Overview")
metrics = {
    "Overall % Completed": overall_completed,
    "Required Reports Compliance": required_compliance,
    "Overall Performance Measure": overall_performance
}

for title, value in metrics.items():
    percent = min(float(value), 100)
    st.markdown(f"""
    <div style='margin-bottom: 10px;'>
        <strong>{title}: {percent:.1f}%</strong>
        <div style='background-color: #ddd; border-radius: 20px; height: 20px; width: 100%;'>
            <div style='width: {percent}%; background-color: #4CAF50; height: 100%; border-radius: 20px;'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ✅ Wrap everything else in try/except
try:
    df = pd.read_csv(sheet_url)
    df['Date'] = pd.to_datetime(df['Date'].astype(str), errors='coerce')
    df = df.dropna(subset=['Date'])
    df['DateLabel'] = df['Date'].dt.strftime('%-m/%-d')
    perf_df = pd.read_csv(performance_sheet_url)

    latest_overall_score = df['Overall % Completed (MHOs & Discharges)'].iloc[-1]
    latest_reports_compliance = df['Required Reports Compliance'].iloc[-1]
    overall_perf_measure = perf_df['Score'].dropna().iloc[-1]

    # Line Chart: Overall Score
    st.subheader("📈 Overall Score YTD")
    st.markdown("This score is the overall performance score for completed POMs (MHOs) and Discharges.")
    fig1, ax1 = plt.subplots()
    ax1.plot(df['DateLabel'], df['Overall % Completed (MHOs & Discharges)'], marker='o', color='green')
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Overall Score")
    ax1.set_title("Overall Score Trend YTD")
    ax1.grid(True)
    plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig1)

    # Completed Records Chart
    st.subheader("✅ Completed Records YTD")
    st.markdown("This is the amount of POMs (MHOs) that have been submitted since January.")
    completed = df['Total Possible'] - df['Missing records']
    fig2, ax2 = plt.subplots()
    ax2.plot(df['DateLabel'], completed, marker='o', color='green')
    ax2.set_title("Completed Records YTD")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Count")
    ax2.grid(True)
    plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig2)

    # Missing Records Chart
    st.subheader("❌ Missing Records")
    st.markdown("This is the amount of records that are missing. Our goal is to be as close to zero as we can!")
    missing = df['Missing records']
    fig3, ax3 = plt.subplots()
    ax3.plot(df['DateLabel'], missing, marker='s', color='green')
    ax3.set_title("Missing Records YTD")
    ax3.set_xlabel("Date")
    ax3.set_ylabel("Count")
    ax3.grid(True)
    plt.setp(ax3.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig3)

    # Reports Compliance Chart
    st.subheader("📄 Required Contractual Reports Compliance")
    st.markdown("*Compliance is measured by computing the number of items submitted ON TIME divided by TOTAL items.*")
    fig4, ax4 = plt.subplots()
    ax4.plot(df['DateLabel'], df['Required Reports Compliance'], marker='o', color='green')
    ax4.set_xlabel("Date")
    ax4.set_ylabel("Compliance %")
    ax4.set_title("Contractual Reports Compliance Over Time")
    ax4.grid(True)
    plt.setp(ax4.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig4)

    # Performance Measures Bar Chart
    st.subheader("📊 Overall Performance Measures")
    perf_df['Label'] = perf_df['Measure'] + " - " + perf_df['Description']
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    x = range(len(perf_df))
    ax5.bar([i - 0.2 for i in x], perf_df['Score'], width=0.4, label='Score', color='green')
    ax5.bar([i + 0.2 for i in x], perf_df['Target'], width=0.4, label='Target', color='gray')
    ax5.set_xticks(x)
    ax5.set_xticklabels(perf_df['Label'], rotation=45, ha='right', fontsize=8)
    ax5.set_ylabel("Value")
    ax5.set_title("Performance Measure Score vs Target")
    ax5.legend()
    st.pyplot(fig5)

    # Data Preview
    with st.expander("🔍 View Raw Data"):
        st.dataframe(df)

except Exception as e:
    st.error(f"An error occurred while loading the Google Sheet: {e}")
