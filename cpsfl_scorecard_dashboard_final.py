import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import urllib.request

st.set_page_config(page_title="CPSFL Scorecard Dashboard", layout="wide")

# Custom CSS to center header and style
st.markdown("""
    <style>
        .centered-title {
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            margin-top: 20px;
        }
        .subtitle {
            text-align: center;
            font-size: 20px;
            color: #2E7D32;
            margin-bottom: 30px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='centered-title'>CPSFL Scorecard Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Thriving Residents. Strong Communities.</div>", unsafe_allow_html=True)

# Helper function to load Google Sheet CSV
@st.cache_data
def load_sheet(url):
    return pd.read_csv(url)

# Google Sheets published URLs (CSV links)
tabs = {
    "Summary Metrics": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTVohW51_sRlF_mD7xijTJ8hW47jtIx2-9Ff2mNytnLKWTt926hR_yTtSihI7N2gu9EnEGP3wvjK43v/pub?gid=965565385&single=true&output=csv",
    "Overall Score Breakdown": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTVohW51_sRlF_mD7xijTJ8hW47jtIx2-9Ff2mNytnLKWTt926hR_yTtSihI7N2gu9EnEGP3wvjK43v/pub?gid=209468973&single=true&output=csv",
    "Reports Compliance Breakdown": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTVohW51_sRlF_mD7xijTJ8hW47jtIx2-9Ff2mNytnLKWTt926hR_yTtSihI7N2gu9EnEGP3wvjK43v/pub?gid=467511660&single=true&output=csv",
    "Performance Measure Breakdown": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTVohW51_sRlF_mD7xijTJ8hW47jtIx2-9Ff2mNytnLKWTt926hR_yTtSihI7N2gu9EnEGP3wvjK43v/pub?gid=401432916&single=true&output=csv",
    "Waitlist Overview": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTVohW51_sRlF_mD7xijTJ8hW47jtIx2-9Ff2mNytnLKWTt926hR_yTtSihI7N2gu9EnEGP3wvjK43v/pub?gid=869606256&single=true&output=csv",
    "Waitlist by Program": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTVohW51_sRlF_mD7xijTJ8hW47jtIx2-9Ff2mNytnLKWTt926hR_yTtSihI7N2gu9EnEGP3wvjK43v/pub?gid=1961299205&single=true&output=csv"
}

# Load summary metrics
try:
    summary_df = load_sheet(tabs["Summary Metrics"])
    summary_df = summary_df.drop(columns=summary_df.columns[0], errors='ignore')  # Remove line number columns if present

    # Half-circle gauge chart function
    def plot_half_circle(title, value):
        fig, ax = plt.subplots(figsize=(3.5, 2.5))
        theta = np.linspace(-np.pi, 0, 100)
        x = np.cos(theta)
        y = np.sin(theta)
        ax.plot(x, y, color='lightgray', linewidth=20, solid_capstyle='round')

        end_angle = (-np.pi) + (value / 100.0) * np.pi
        filled_theta = np.linspace(-np.pi, end_angle, 100)
        fx = np.cos(filled_theta)
        fy = np.sin(filled_theta)
        ax.plot(fx, fy, color='green', linewidth=20, solid_capstyle='round')

        ax.text(0, -0.2, f"{value:.1f}%", ha='center', va='center', fontsize=16, fontweight='bold')
        ax.set_title(title, fontsize=12)
        ax.set_aspect('equal')
        ax.axis('off')
        return fig

    # Display 3 half-circle gauges
    col1, col2, col3 = st.columns(3)
    with col1:
        val1 = summary_df['Overall % Completed'].dropna().iloc[-1]
        st.pyplot(plot_half_circle("Overall % Completed", val1))
    with col2:
        val2 = summary_df['Required Reports Compliance'].dropna().iloc[-1]
        st.pyplot(plot_half_circle("Required Reports Compliance", val2))
    with col3:
        val3 = summary_df['Overall Performance Measure'].dropna().iloc[-1]
        st.pyplot(plot_half_circle("Overall Performance Measure", val3))

except Exception as e:
    st.error(f"Error loading data: {e}")
