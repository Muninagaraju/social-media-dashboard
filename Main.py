import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Social Media Dashboard",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("social_media_addiction.csv")
    return df

df = load_data()

# =========================
# TITLE
# =========================
st.title("📊 Social Media Addiction Dashboard")

st.write("Dashboard deployed successfully 🚀")

# =========================
# METRICS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Total Users", len(df))

col2.metric(
    "Avg Usage Hours",
    round(df["DailySocialMediaHours"].mean(), 2)
)

col3.metric(
    "Avg Sleep Hours",
    round(df["SleepHours"].mean(), 2)
)

# =========================
# PLATFORM ANALYSIS
# =========================
platform = df["PlatformUsage"].value_counts().reset_index()

platform.columns = ["Platform", "Count"]

fig = px.bar(
    platform,
    x="Platform",
    y="Count",
    color="Platform",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# DATA PREVIEW
# =========================
st.subheader("Dataset Preview")

st.dataframe(df.head())