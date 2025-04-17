import streamlit as st
import pandas as pd
from utils.topics import TOPICS
from utils.summary_generator import get_summary, get_why_it_matters
from pandas_datareader import wb
import plotly.graph_objects as go

st.set_page_config(page_title="Progress Over Time", layout="centered")
st.title("🌍 How Has the World Changed?")

# Sidebar topic selector
topic_names = list(TOPICS.keys())
selected_topic = st.selectbox("Choose a topic to explore:", topic_names)

topic_info = TOPICS[selected_topic]
indicator = topic_info["indicator"]

# Fetch global data from World Bank
st.write("⏳ Fetching historical data...")

df = wb.download(indicator=indicator, country='WLD', start=1920, end=2020).reset_index()
df = df.rename(columns={indicator: "value"})
df["year"] = df["year"].astype(int)  # 🛠 Fix here
df = df.sort_values("year")
df = df[df["value"].notnull()]

# Extract specific year values
target_years = [1920, 1970, 2020]
year_values = {}
for year in target_years:
    closest = df.iloc[(df["year"] - year).abs().argsort()[:1]]
    year_values[year] = round(closest["value"].values[0], 2)

# Show chart
st.subheader(topic_info["description"])
fig = go.Figure()
fig.add_trace(go.Scatter(x=df["year"], y=df["value"], mode='lines+markers'))
fig.update_layout(
    yaxis_title=topic_info["unit"],
    xaxis_title="Year",
    height=400,
)
st.plotly_chart(fig)

# Generate and display AI summary
st.subheader("📈 Summary")
summary = get_summary(selected_topic, year_values)
st.markdown(summary)

# Generate and display the "Why does this matter?" section
st.subheader("🧐 Why Does This Matter?")
why_it_matters = get_why_it_matters(selected_topic, year_values)
st.markdown(why_it_matters)

# Sources and Methodology section
st.subheader("📚 Sources & Methodology")
st.markdown(f"**Source:** {topic_info['source']}")
st.markdown(f"**Data Link:** [Click here]({topic_info['source_link']})")
st.markdown(f"**Methodology:** {topic_info['methodology']}")