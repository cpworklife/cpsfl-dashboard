import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

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

# Dark mode toggle (simulated with background color swap)
dark_mode = st.toggle("🌙 Dark Mode")
if dark_mode:
    st.markdown("""
    <style>
        body { background-color: #121212; color: white; }
        .stApp { background-color: #121212; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 CPSFL Scorecard Dashboard")

# Load data directly from Google Sheets CSV link
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTVohW51_sRlF_mD7xijTJ8hW47jtIx2-9Ff2mNytnLKWTt926hR_yTtSihI7N2gu9EnEGP3wvjK43v/pub?output=csv"

# Refresh button
if st.button("🔄 Refresh Data"):
    st.rerun()

try:
    df = pd.read_csv(sheet_url)

    # Safely convert any values in Date to string before parsing
    df['Date'] = pd.to_datetime(df['Date'].astype(str), errors='coerce')
    df = df.dropna(subset=['Date'])  # Drop any rows where date couldn't be parsed
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

    # Completed Chart
    st.subheader("✅ Completed Records")
    completed = df['Total Possible'] - df['Missing records']
    fig2a, ax2a = plt.subplots()
    ax2a.plot(df['DateLabel'], completed, marker='o', label='Completed', color='blue')
    ax2a.set_title("Completed Records Over Time")
    ax2a.set_xlabel("Date")
    ax2a.set_ylabel("Count")
    ax2a.grid(True)
    plt.setp(ax2a.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig2a)

    # Missing Chart
    st.subheader("❌ Missing Records")
    missing = df['Missing records']
    fig2b, ax2b = plt.subplots()
    ax2b.plot(df['DateLabel'], missing, marker='s', label='Missing', color='red')
    ax2b.set_title("Missing Records Over Time")
    ax2b.set_xlabel("Date")
    ax2b.set_ylabel("Count")
    ax2b.grid(True)
    plt.setp(ax2b.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig2b)

    # Combo Chart
    st.subheader("📉 Scorecard Metrics Over Time")
    fig3, ax3 = plt.subplots()
    ax3.plot(df['DateLabel'], df['Overall % Completed (MHOs & Discharges)'], label='Overall Score Trend', marker='o', color='green')
    ax3.plot(df['DateLabel'], df['Required Reports Compliance'], label='MHO Discharges Over Time', marker='s')
    ax3.set_ylim(60, 105)
    ax3.set_yticks(range(60, 106, 5))
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

    # AI Summary of trends
    st.subheader("🧠 AI Trend Summary")
    avg_score = df['Overall % Completed (MHOs & Discharges)'].mean()
    recent_score = df['Overall % Completed (MHOs & Discharges)'].iloc[-1]
    trend = "📈 improving" if recent_score > avg_score else "📉 declining"
    st.markdown(f"The overall score is currently at **{recent_score:.2f}%**, which is {trend} compared to the average of **{avg_score:.2f}%**.")

except Exception as e:
    st.error(f"An error occurred while loading the Google Sheet: {e}")
