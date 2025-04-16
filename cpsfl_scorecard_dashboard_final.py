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
performance_sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTVohW51_sRlF_mD7xijTJ8hW47jtIx2-9Ff2mNytnLKWTt926hR_yTtSihI7N2gu9EnEGP3wvjK43v/pub?gid=460550068&single=true&output=csv"
df['Date'] = pd.to_datetime(df['Date'].astype(str), errors='coerce')
df = df.dropna(subset=['Date'])
df['DateLabel'] = df['Date'].dt.strftime('%-m/%-d')
perf_df = pd.read_csv(performance_sheet_url)

# Gauge-style Overview (dynamic values)\1
# Custom Half-Circle Gauge Charts
def draw_gauge(value, label):
fig, ax = plt.subplots()
ax.barh(0, value, height=1, left=0, color='green')
ax.set_xlim(0, 100)
ax.set_ylim(-0.5, 0.5)
ax.axis('off')
ax.text(50, 0, f"{value:.2f}%", ha='center', va='center', fontsize=16, fontweight='bold')
ax.set_title(label, fontsize=12)
return fig

col1, col2, col3 = st.columns(3)
with col1:
st.pyplot(draw_gauge(latest_overall_score, "Overall % Completed"))
with col2:
st.pyplot(draw_gauge(latest_reports_compliance, "Required Reports Compliance"))
with col3:
st.pyplot(draw_gauge(overall_perf_measure, "Overall Performance Measure"))
st.metric(label="Overall Performance Measure", value=f"{overall_perf_measure:.2f}%")
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTVohW51_sRlF_mD7xijTJ8hW47jtIx2-9Ff2mNytnLKWTt926hR_yTtSihI7N2gu9EnEGP3wvjK43v/pub?output=csv"
performance_sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTVohW51_sRlF_mD7xijTJ8hW47jtIx2-9Ff2mNytnLKWTt926hR_yTtSihI7N2gu9EnEGP3wvjK43v/pub?gid=460550068&single=true&output=csv"

# Refresh button
if st.button("🔄 Refresh Data"):
st.rerun()

try:
df = pd.read_csv(sheet_url)
df['Date'] = pd.to_datetime(df['Date'].astype(str), errors='coerce')
df = df.dropna(subset=['Date'])
df['DateLabel'] = df['Date'].dt.strftime('%-m/%-d')

# Line Chart: Overall Score
st.subheader("📈 Overall Score Over Time YTD")
st.markdown("This score is the overall performance score for completed POMs (MHOs) and Discharges. This score reflects the percentage of POMs and Discharges that have been accurately completed to date. Below you will find a breakdown of how many were submitted and how many are still outstanding or past due.")
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
ax2.plot(df['DateLabel'], completed, marker='o', label='Completed', color='green')
ax2.set_title("Completed Records Over Time")
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
ax3.plot(df['DateLabel'], missing, marker='s', label='Missing', color='green')
ax3.set_title("Missing Records YTD")
ax3.set_xlabel("Date")
ax3.set_ylabel("Count")
ax3.grid(True)
plt.setp(ax3.get_xticklabels(), rotation=45, ha='right')
st.pyplot(fig3)

# Reports Compliance Chart
st.subheader("📄 Required Contractual Reports Compliance")
st.markdown("*Total does NOT include items pending REVIEW. Compliance is measured by computing the number of items submitted ON TIME divided by TOTAL items.*")
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
perf_df = pd.read_csv(performance_sheet_url)
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

# AI Summary of trends
st.subheader("🧠 AI Trend Summary")
avg_score = df['Overall % Completed (MHOs & Discharges)'].mean()
recent_score = df['Overall % Completed (MHOs & Discharges)'].iloc[-1]
trend = "📈 improving" if recent_score > avg_score else "📉 declining"
st.markdown(f"The overall score is currently at **{recent_score:.2f}%**, which is {trend} compared to the average of **{avg_score:.2f}%**.")

except Exception as e:
st.error(f"An error occurred while loading the Google Sheet: {e}")
