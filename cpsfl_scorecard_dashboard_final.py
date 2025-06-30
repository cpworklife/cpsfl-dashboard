import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Streamlit page config
st.set_page_config(page_title="CPSFL Scorecard Dashboard", layout="wide")

# Centered title
st.markdown("""
    <h1 style='text-align: center;'>CPSFL Scorecard Dashboard</h1>
    <h4 style='text-align: center;'>Thriving Residents. Strong Communities.</h4>
""", unsafe_allow_html=True)

# Google Sheet setup
base_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTVohW51_sRlF_mD7xijTJ8hW47jtIx2-9Ff2mNytnLKWTt926hR_yTtSihI7N2gu9EnEGP3wvjK43v/pub?gid={gid}&single=true&output=csv"
tabs = {
    "Summary Metrics": 965565385,
    "Overall Score Breakdown": 209468973,
    "Reports Compliance Breakdown": 467511660,
    "Performance Measure Breakdown": 401432916,
    "Waitlist Overview": 869606256,
    "Waitlist by Program": 1961299205
}

def load_sheet(gid):
    url = base_url.format(gid=gid)
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df.reset_index(drop=True)

def rainbow_gauge(label, value):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': label},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "green"},
            'steps': [
                {'range': [0, 50], 'color': "#d6f5d6"},
                {'range': [50, 75], 'color': "#a3e4a3"},
                {'range': [75, 100], 'color': "#60c060"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=0), height=300)
    return fig

# SECTION 1 – Summary Metrics
st.header("📊 Summary Metrics")
try:
    summary_df = load_sheet(tabs["Summary Metrics"])
    summary_df["Score"] = summary_df["Score"].astype(str).str.replace("%", "").astype(float)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(rainbow_gauge(summary_df.loc[0, "Description"], summary_df.loc[0, "Score"]), use_container_width=True)
    with col2:
        st.plotly_chart(rainbow_gauge(summary_df.loc[1, "Description"], summary_df.loc[1, "Score"]), use_container_width=True)
    with col3:
        st.plotly_chart(rainbow_gauge(summary_df.loc[2, "Description"], summary_df.loc[2, "Score"]), use_container_width=True)

    st.dataframe(summary_df, use_container_width=True, hide_index=True)
except Exception as e:
    st.error(f"Error loading Summary Metrics: {e}")

# Generic loader for all other sections
def render_section(header, tab_name, note=None):
    st.header(header)
    try:
        df = load_sheet(tabs[tab_name])
        if note:
            st.markdown(note)
        st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Error loading {tab_name}: {e}")

render_section("📈 Overall Score Breakdown", "Overall Score Breakdown",
               "This score is the overall performance score for completed POMs (MHOs) and Discharges.")

render_section("📄 Reports Compliance Breakdown", "Reports Compliance Breakdown",
               "*Compliance is measured by computing the number of items submitted ON TIME divided by TOTAL items.*")

render_section("📊 Performance Measure Breakdown", "Performance Measure Breakdown")
render_section("⏳ Waitlist Overview", "Waitlist Overview")
render_section("🏥 Waitlist by Program", "Waitlist by Program")
