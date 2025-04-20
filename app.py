import streamlit as st
import pandas as pd
from utils.topics import TOPICS
from utils.summary_generator import get_summary, get_why_it_matters
from utils.search_utils import find_matching_topics
from pandas_datareader import wb
import plotly.graph_objects as go

st.set_page_config(page_title="Progress Over Time", layout="centered")
st.title("🌍 How Has the World Changed?")

# 🔍 Search section
st.markdown("### 🔎 Search for a topic")
user_query = st.text_input("Type a keyword like 'pollution', 'poverty', or 'death':")

selected_topic = None

if user_query:
    matches = find_matching_topics(user_query)
    if matches:
        selected_topic = st.selectbox("Did you mean one of these topics?", matches)
    else:
        st.warning("No matching topics found. Try different keywords.")
else:
    # Fallback if nothing typed: show dropdown of all topics
    topic_names = list(TOPICS.keys())
    selected_topic = st.selectbox("Choose a topic to explore:", topic_names)

if selected_topic:
    topic_info = TOPICS[selected_topic]
    indicator = topic_info["indicator"]

    st.write("⏳ Fetching historical data...")

    df = wb.download(indicator=indicator, country='WLD', start=1920, end=2020).reset_index()
    df = df.rename(columns={indicator: "value"})
    df["year"] = df["year"].astype(int)
    df = df.sort_values("year")
    df = df[df["value"].notnull()]

    target_years = [1920, 1970, 2020]
    year_values = {}
    for year in target_years:
        closest = df.iloc[(df["year"] - year).abs().argsort()[:1]]
        year_values[year] = round(closest["value"].values[0], 2)

    st.subheader(topic_info["description"])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["year"], y=df["value"], mode='lines+markers'))
    fig.update_layout(
        yaxis_title=topic_info["unit"],
        xaxis_title="Year",
        height=400,
    )
    st.plotly_chart(fig)

    # 📈 Summary
    st.subheader("📈 Summary")
    summary = get_summary(selected_topic, year_values)
    st.markdown(summary)

    # 🧐 Why Does This Matter
    st.subheader("🧐 Why Does This Matter?")
    why_it_matters = get_why_it_matters(selected_topic, year_values)
    st.markdown(why_it_matters)

    # 📚 Sources
    st.subheader("📚 Sources & Methodology")
    st.markdown(f"**Source:** {topic_info['source']}")
    st.markdown(f"**Data Link:** [Click here]({topic_info['source_link']})")
    st.markdown(f"**Methodology:** {topic_info['methodology']}")