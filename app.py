import streamlit as st
import pandas as pd
import json
import os
from pathlib import Path
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="VarsenseAI Dashboard", layout="wide", page_icon="✨")

# Load Data
@st.cache_data
def load_data(filename):
    path = Path("mock_data") / filename
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

employees = load_data("employees.json")
projects = load_data("projects.json")
meetings = load_data("meetings.json")

employee_dict = {emp["id"]: emp for emp in employees}

# Logic for Attribution and Costs
if 'attribution_results' not in st.session_state:
    st.session_state.attribution_results = []

if 'agent_reports' not in st.session_state:
    st.session_state.agent_reports = []

def get_project_for_meeting(title):
    for att in reversed(st.session_state.attribution_results):
        if att.get("request_title") == title:
            return att["project_name"]
    return "Unassigned"

def get_meeting_costs():
    costs = []
    for m in meetings:
        dur_hrs = m["duration_minutes"] / 60.0
        total_rate = sum(employee_dict.get(aid, {}).get("hourly_rate", 0) for aid in m["attendees"])
        cost = dur_hrs * total_rate
        
        costs.append({
            "meeting_id": m["id"],
            "meeting_title": m["title"],
            "project_name": get_project_for_meeting(m["title"]),
            "duration_minutes": m["duration_minutes"],
            "attendee_count": len(m["attendees"]),
            "meeting_cost": round(cost, 2),
            "date": m.get("date", "2026-01-01T00:00:00Z")
        })
    return costs

# UI Configuration
st.title("VarsenseAI Intelligence Engine")
st.markdown("Track the hidden financial costs of corporate meetings and attribute them to projects.")

all_costs = get_meeting_costs()

if not all_costs:
    st.warning("No meeting data found.")
    st.stop()

df_costs = pd.DataFrame(all_costs)
df_costs['date_obj'] = pd.to_datetime(df_costs['date']).dt.date

# Add Date Filter
st.sidebar.header("Filters")
min_date = df_costs['date_obj'].min()
max_date = df_costs['date_obj'].max()

date_range = st.sidebar.date_input(
    "Select Date Range for Analysis",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range
    df_costs = df_costs[(df_costs['date_obj'] >= start_date) & (df_costs['date_obj'] <= end_date)]
elif len(date_range) == 1:
    start_date = date_range[0]
    df_costs = df_costs[df_costs['date_obj'] == start_date]

if df_costs.empty:
    st.warning("No meetings found in this date range. Please select a wider range.")
    st.stop()

# KPI Cards
st.subheader("Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

total_projects = len(projects)
total_meetings = len(meetings)
total_hr_cost = df_costs["meeting_cost"].sum()
avg_cost = df_costs["meeting_cost"].mean()

col1.metric("Total Projects", total_projects)
col2.metric("Total Meetings", total_meetings)
col3.metric("Total HR Cost", f"${total_hr_cost:,.2f}")
col4.metric("Avg Meeting Cost", f"${avg_cost:,.2f}")

st.divider()

# Charts
st.subheader("Cost Analysis")
colA, colB = st.columns(2)

with colA:
    st.markdown("### Cost by Project")
    project_costs = df_costs.groupby("project_name")["meeting_cost"].sum().reset_index()
    if not project_costs.empty:
        st.bar_chart(project_costs.set_index("project_name"))

with colB:
    st.markdown("### Monthly Trend")
    df_costs['month'] = pd.to_datetime(df_costs['date']).dt.to_period('M').astype(str)
    trend = df_costs.groupby('month')['meeting_cost'].sum().reset_index()
    if not trend.empty:
        st.line_chart(trend.set_index('month'))

st.divider()

st.subheader("Meetings Data")
st.dataframe(df_costs, use_container_width=True)

st.divider()

# AI Agent Actions
st.subheader("AI Agent Insights")
api_key = os.getenv("GEMINI_API_KEY")

if st.button("Run Executive Analysis"):
    if not api_key:
        st.error("Please set GEMINI_API_KEY in your environment or .env file.")
    else:
        with st.spinner("Agent is analyzing the data..."):
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            context = {
                "total_cost": total_hr_cost,
                "total_meetings": total_meetings,
                "project_costs": project_costs.to_dict('records') if not project_costs.empty else []
            }
            
            prompt = f"""
            You are an expert Executive Financial Analyst AI.
            Analyze the following corporate meeting HR cost data and write a short, punchy executive summary (max 3 paragraphs).
            Identify any major "Cost Anomalies" - e.g., a specific project burning too much budget on meetings.
            Format your response in Markdown. Use bolding for emphasis. Be direct and analytical.
            
            Data:
            {json.dumps(context, indent=2)}
            """
            
            try:
                response = model.generate_content(prompt)
                st.session_state.agent_reports.insert(0, {
                    "timestamp": datetime.utcnow().isoformat(),
                    "content": response.text
                })
            except Exception as e:
                st.error(f"Failed to generate insight: {e}")

if st.session_state.agent_reports:
    latest_report = st.session_state.agent_reports[0]
    st.success(f"Report generated at {latest_report['timestamp']}")
    st.markdown(latest_report['content'])
