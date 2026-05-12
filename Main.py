# python -m streamlit run webpage.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from streamlit_extras.metric_cards import style_metric_cards

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Social Media Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>

/* Main Background */
.main {
    background-color: #0E1117;
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* KPI Cards */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1f2937, #111827);
    border: 1px solid #374151;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
}

/* Metric Label */
[data-testid="metric-container"] label {
    color: #9CA3AF !important;
    font-size: 16px !important;
}

/* Metric Value */
[data-testid="metric-container"] div {
    color: white !important;
    font-size: 28px !important;
    font-weight: bold !important;
}

/* Plotly Charts */
.stPlotlyChart {
    background-color: #1F2937;
    padding: 15px;
    border-radius: 18px;
    border: 1px solid #374151;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 15px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR MENU
# =========================================================
with st.sidebar:

    st.title("📱 Dashboard")

    selected = option_menu(
        menu_title=None,
        options=[
            "Overview",
            "Mental Health",
            "Analytics"
        ],
        icons=[
            "house",
            "activity",
            "bar-chart"
        ],
        default_index=0
    )

# =========================================================
# DATABASE CONNECTION
# =========================================================

# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():

    df = pd.read_csv("social_media_addiction.csv")

    numeric_cols = [
        "Age",
        "DailySocialMediaHours",
        "SleepHours",
        "StressLevel",
        "AnxietyLevel",
        "AddictionLevel",
        "AcademicPerformance",
        "SocialInteractionLevel"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df.fillna(0, inplace=True)

    return df

df = load_data()

# =========================================================
# SIDEBAR FILTERS
# =========================================================
st.sidebar.header("🔍 Filters")

gender_filter = st.sidebar.multiselect(
    "Select Gender",
    df["Gender"].unique(),
    default=df["Gender"].unique()
)

platform_filter = st.sidebar.multiselect(
    "Select Platform",
    df["PlatformUsage"].unique(),
    default=df["PlatformUsage"].unique()
)

df = df[
    (df["Gender"].isin(gender_filter)) &
    (df["PlatformUsage"].isin(platform_filter))
]

# =========================================================
# DASHBOARD TITLE
# =========================================================
st.title("📊 Social Media Addiction Dashboard")

st.markdown("""
Analyze social media addiction trends,
mental health patterns,
sleep quality,
and academic performance.
""")

# =========================================================
# KPI METRICS
# =========================================================
st.subheader("📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Users",
    f"{len(df):,}"
)

col2.metric(
    "Avg Usage Hours",
    round(df["DailySocialMediaHours"].mean(), 2)
)

col3.metric(
    "Avg Sleep Hours",
    round(df["SleepHours"].mean(), 2)
)

col4.metric(
    "Avg Stress Level",
    round(df["StressLevel"].mean(), 2)
)

style_metric_cards(
    background_color="#111827",
    border_left_color="#06B6D4",
    border_color="#374151"
)

# =========================================================
# PLATFORM ANALYSIS
# =========================================================
st.subheader("📱 Platform Usage Analysis")

platform = df["PlatformUsage"].value_counts().reset_index()

platform.columns = ["Platform", "Count"]

col1, col2 = st.columns(2)

# ---------------- BAR CHART ----------------
fig1 = px.bar(
    platform,
    x="Platform",
    y="Count",
    color="Platform",
    text="Count",
    template="plotly_dark"
)

fig1.update_layout(
    height=450,
    paper_bgcolor="#1F2937",
    plot_bgcolor="#1F2937",
    font_color="white"
)

col1.plotly_chart(
    fig1,
    use_container_width=True
)

# ---------------- DONUT CHART ----------------
fig2 = px.pie(
    platform,
    names="Platform",
    values="Count",
    hole=0.6,
    template="plotly_dark"
)

fig2.update_layout(
    height=450,
    paper_bgcolor="#1F2937",
    font_color="white"
)

col2.plotly_chart(
    fig2,
    use_container_width=True
)

# =========================================================
# CORRELATION HEATMAP
# =========================================================
st.subheader("🔥 Correlation Heatmap")

corr = df[[
    "DailySocialMediaHours",
    "SleepHours",
    "StressLevel",
    "AnxietyLevel",
    "AcademicPerformance"
]].corr()

fig3 = go.Figure(
    data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale="RdBu"
    )
)

fig3.update_layout(
    template="plotly_dark",
    height=500,
    paper_bgcolor="#1F2937",
    plot_bgcolor="#1F2937",
    font_color="white"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# =========================================================
# MENTAL HEALTH ANALYSIS
# =========================================================
st.subheader("🧠 Mental Health Analysis")

mental = df.groupby("Gender")[[
    "StressLevel",
    "AnxietyLevel"
]].mean().reset_index()

fig4 = px.bar(
    mental,
    x="Gender",
    y=["StressLevel", "AnxietyLevel"],
    barmode="group",
    template="plotly_dark"
)

fig4.update_layout(
    height=450,
    paper_bgcolor="#1F2937",
    plot_bgcolor="#1F2937",
    font_color="white"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# =========================================================
# STRESS DISTRIBUTION
# =========================================================
st.subheader("📦 Stress Distribution")

fig5 = px.box(
    df,
    x="Gender",
    y="StressLevel",
    color="Gender",
    template="plotly_dark"
)

fig5.update_layout(
    height=450,
    paper_bgcolor="#1F2937",
    plot_bgcolor="#1F2937",
    font_color="white"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# =========================================================
# DEPRESSION DISTRIBUTION
# =========================================================
st.subheader("😔 Depression Distribution")

dep = df["DepressionLabel"].value_counts().reset_index()

dep.columns = ["Label", "Count"]

fig6 = px.bar(
    dep,
    x="Label",
    y="Count",
    color="Label",
    text="Count",
    template="plotly_dark"
)

fig6.update_layout(
    height=450,
    paper_bgcolor="#1F2937",
    plot_bgcolor="#1F2937",
    font_color="white"
)

st.plotly_chart(
    fig6,
    use_container_width=True
)

# =========================================================
# DAILY SOCIAL MEDIA HOURS
# =========================================================
st.subheader("⏰ Daily Social Media Usage")

fig7 = px.histogram(
    df,
    x="DailySocialMediaHours",
    nbins=20,
    color="Gender",
    template="plotly_dark"
)

fig7.update_layout(
    height=450,
    paper_bgcolor="#1F2937",
    plot_bgcolor="#1F2937",
    font_color="white"
)

st.plotly_chart(
    fig7,
    use_container_width=True
)

# =========================================================
# DATA TABLE
# =========================================================
st.subheader("📄 Dataset Preview")

st.dataframe(
    df.head(20),
    use_container_width=True
)

# =========================================================
# DOWNLOAD BUTTON
# =========================================================
csv = df.to_csv(index=False)

st.download_button(
    label="📥 Download Dataset",
    data=csv,
    file_name="social_media_data.csv",
    mime="text/csv"
)

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")

st.caption(
    "Developed by Muninagaraju | Data Analyst Portfolio Project"
)