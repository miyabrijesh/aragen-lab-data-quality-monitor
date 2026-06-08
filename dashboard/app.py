import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Lab Data Quality Monitor",
    page_icon="🧪",
    layout="wide"
)

# ==================================================
# CUSTOM STYLING
# ==================================================

st.markdown("""
<style>
.metric-card {
    padding: 15px;
    border-radius: 10px;
    background-color: #1e1e1e;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# TITLE
# ==================================================

st.title("🧪 Lab Data Quality Monitor")
st.markdown("### Aragen Life Sciences Internship Assignment")

st.markdown("---")

# ==================================================
# DATABASE CONNECTION
# ==================================================

conn = sqlite3.connect(
    "../database/lab_quality_task3.db"
)

# ==================================================
# LOAD TABLES
# ==================================================

fact_df = pd.read_sql(
    "SELECT * FROM fact_lab_measurements",
    conn
)

failed_df = pd.read_sql(
    "SELECT * FROM failed_records",
    conn
)

dim_lab = pd.read_sql(
    "SELECT * FROM dim_lab",
    conn
)

# ==================================================
# DATE CONVERSION
# ==================================================

fact_df["experiment_date"] = pd.to_datetime(
    fact_df["experiment_date"],
    errors="coerce"
)

# ==================================================
# KPI SECTION
# ==================================================

overall_score = round(
    fact_df["quality_score"].mean(),
    2
)

total_records = len(fact_df)

failed_records = len(
    fact_df[fact_df["quality_score"] < 100]
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Overall Quality Score",
        f"{overall_score}%"
    )

with col2:
    st.metric(
        "Total Records",
        f"{total_records:,}"
    )

with col3:
    st.metric(
        "Failed Records",
        f"{failed_records:,}"
    )

st.markdown("---")

# ==================================================
# SIDEBAR FILTERS
# ==================================================

st.sidebar.header("Filters")

severity_filter = st.sidebar.multiselect(
    "Severity",
    options=sorted(
        fact_df["severity"].dropna().unique()
    ),
    default=sorted(
        fact_df["severity"].dropna().unique()
    )
)

lab_filter = st.sidebar.multiselect(
    "Lab",
    options=sorted(
        fact_df["lab_key"].dropna().unique()
    ),
    default=sorted(
        fact_df["lab_key"].dropna().unique()
    )
)

instrument_filter = st.sidebar.multiselect(
    "Instrument",
    options=sorted(
        fact_df["instrument_key"].dropna().unique()
    ),
    default=sorted(
        fact_df["instrument_key"].dropna().unique()
    )
)

date_range = st.sidebar.date_input(
    "Date Range",
    value=(
        fact_df["experiment_date"].min(),
        fact_df["experiment_date"].max()
    )
)

# ==================================================
# APPLY FILTERS
# ==================================================

start_date, end_date = date_range

filtered_df = fact_df[
    (fact_df["severity"].isin(severity_filter))
    &
    (fact_df["lab_key"].isin(lab_filter))
    &
    (fact_df["instrument_key"].isin(instrument_filter))
    &
    (fact_df["experiment_date"].dt.date >= start_date)
    &
    (fact_df["experiment_date"].dt.date <= end_date)
].copy()

# ==================================================
# QUALITY BY LAB
# ==================================================

lab_quality = (
    filtered_df
    .groupby("lab_key")["quality_score"]
    .mean()
    .reset_index()
)

lab_quality = lab_quality.merge(
    dim_lab,
    on="lab_key",
    how="left"
)

fig_lab = px.bar(
    lab_quality,
    x="lab_name",
    y="quality_score",
    title="Quality Breakdown by Lab",
    text_auto=".2f"
)

st.plotly_chart(
    fig_lab,
    use_container_width=True
)

# ==================================================
# QUALITY BY INSTRUMENT
# ==================================================

instrument_quality = (
    filtered_df
    .groupby("instrument_key")["quality_score"]
    .mean()
    .reset_index()
)

fig_inst = px.bar(
    instrument_quality,
    x="instrument_key",
    y="quality_score",
    title="Quality Breakdown by Instrument",
    text_auto=".2f"
)

st.plotly_chart(
    fig_inst,
    use_container_width=True
)

# ==================================================
# QUALITY OVER TIME
# ==================================================

trend = (
    filtered_df
    .groupby("experiment_date")["quality_score"]
    .mean()
    .reset_index()
)

fig_trend = px.line(
    trend,
    x="experiment_date",
    y="quality_score",
    title="Quality Score Over Time",
    markers=True
)

st.plotly_chart(
    fig_trend,
    use_container_width=True
)

# ==================================================
# SEVERITY DISTRIBUTION
# ==================================================

severity_counts = (
    filtered_df["severity"]
    .value_counts()
    .reset_index()
)

severity_counts.columns = [
    "severity",
    "count"
]

fig_severity = px.pie(
    severity_counts,
    names="severity",
    values="count",
    hole=0.5,
    title="Severity Distribution"
)

st.plotly_chart(
    fig_severity,
    use_container_width=True
)

# ==================================================
# FAILED RECORDS DRILLDOWN
# ==================================================

st.markdown("---")

st.subheader("Failed Records Drilldown")

st.dataframe(
    failed_df,
    use_container_width=True,
    height=500
)

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "Aragen Life Sciences Internship Assignment | Data Quality Monitoring Dashboard"
)

# ==================================================
# CLOSE CONNECTION
# ==================================================

conn.close()
