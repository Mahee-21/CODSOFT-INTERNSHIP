import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from streamlit_lottie import st_lottie
from utils import load_tasks, save_tasks, load_lottie

# Page config
st.set_page_config(page_title="TaskZen To-Do App", layout="wide")

# Pastel theme styling
st.markdown("""
    <style>
        html, body, [class*="css"] {
            background-color: #fdf6f0;
            color: #333;
            font-family: 'Segoe UI', sans-serif;
        }
        .stButton > button {
            background-color: #ffdde1;
            color: black;
            border: none;
            border-radius: 10px;
            padding: 0.6em 1.2em;
            font-size: 16px;
        }
        .stButton > button:hover {
            background-color: #ffcbd1;
            color: white;
        }
        .task-card {
            background-color: #fff9f3;
            padding: 16px;
            border-radius: 15px;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
        }
        .quote-box {
            background-color: #dbeafe;
            color: #1e3a8a;
            padding: 15px;
            border-radius: 12px;
            font-style: italic;
            box-shadow: 1px 1px 8px rgba(0,0,0,0.05);
        }
    </style>
""", unsafe_allow_html=True)


# Load tasks and animation
tasks = load_tasks()
lottie_add = load_lottie("assets/lottie_add.json")
today_str = datetime.today().strftime("%Y-%m-%d")

# Title
st.title("📝 TaskZen – Your Smart Daily Planner")

import random

# 🎯 Motivational Quotes
quotes = [
    "“Start where you are. Use what you have. Do what you can.” – Arthur Ashe",
    "“The secret of getting ahead is getting started.” – Mark Twain",
    "“It always seems impossible until it’s done.” – Nelson Mandela",
    "“Productivity is never an accident.” – Paul Meyer",
    "“Focus on being productive instead of busy.” – Tim Ferriss",
    "“Small progress is still progress.” – Unknown",
    "“You don’t have to be perfect to be amazing.” – Unknown"
]
quote = random.choice(quotes)

st.markdown(f"<div class='quote-box'>{quote}</div>", unsafe_allow_html=True)


# Task entry + Lottie animation
col1, col2 = st.columns([3, 1])
with col1:
    st.subheader("➕ Add a New Task")
    with st.form(key='task_form'):
        title = st.text_input("Task Title")
        due_date = st.date_input("Due Date", value=datetime.today())
        submitted = st.form_submit_button("Add Task")
        if submitted and title:
            new_task = pd.DataFrame([{
                "Title": title,
                "Due Date": due_date.strftime("%Y-%m-%d"),
                "Status": "Pending"
            }])
            tasks = pd.concat([tasks, new_task], ignore_index=True)
            save_tasks(tasks)
            st.success("✅ Task Added!")

with col2:
    st_lottie(lottie_add, height=180)

# Task view filter
st.markdown("---")
view_option = st.selectbox("📂 View Tasks", ["All", "Today", "Completed", "Pending"])

if view_option == "Today":
    filtered_tasks = tasks[tasks["Due Date"] == today_str]
elif view_option == "Completed":
    filtered_tasks = tasks[tasks["Status"] == "Completed"]
elif view_option == "Pending":
    filtered_tasks = tasks[tasks["Status"] == "Pending"]
else:
    filtered_tasks = tasks

# Task cards (grid)
st.subheader("📋 Your Tasks (Grid View)")
cols = st.columns(3)

for i, (index, row) in enumerate(filtered_tasks.iterrows()):
    due = row["Due Date"]
    # Badge color
    if due < today_str:
        due_status = "🔴 Overdue"
        badge_color = "#ffcccc"
    elif due == today_str:
        due_status = "🟡 Today"
        badge_color = "#fff2cc"
    else:
        due_status = "🟢 Upcoming"
        badge_color = "#d9fdd3"

    with cols[i % 3]:
        st.markdown(
            f"""
            <div style='
                background-color:#f9f9f9;
                padding:15px;
                margin-bottom:20px;
                border-radius:15px;
                border: 1px solid #ddd;
            '>
                <h4 style='margin-bottom:5px;'>📝 {row['Title']}</h4>
                <p><b>📅 Due:</b> {due}</p>
                <span style='
                    background-color:{badge_color};
                    padding:3px 8px;
                    border-radius:12px;
                    font-size:12px;
                '>{due_status}</span>
            </div>
            """, unsafe_allow_html=True
        )

        # Status dropdown
        new_status = st.selectbox(
            "Status",
            ["Pending", "Completed"],
            index=["Pending", "Completed"].index(row["Status"]),
            key=f"status_{index}"
        )

        # Delete button
        if st.button("🗑️ Delete", key=f"delete_{index}"):
            tasks = tasks.drop(index)
            save_tasks(tasks)
            st.rerun()

        # Update status
        if new_status != row["Status"]:
            tasks.at[index, "Status"] = new_status
            save_tasks(tasks)
            st.rerun()

# Task progress chart
st.markdown("### 📈 Task Progress")
completed = len(tasks[tasks["Status"] == "Completed"])
total = len(tasks)
progress = int((completed / total) * 100) if total else 0

fig = px.pie(
    names=["Completed", "Pending"],
    values=[completed, total - completed],
    color_discrete_sequence=["green", "red"]
)
st.plotly_chart(fig, use_container_width=True)
st.progress(progress)

# Export
st.markdown("### 📤 Export")
if st.button("📄 Export as CSV"):
    tasks.to_csv("task_export.csv", index=False)
    st.success("✅ Exported as CSV!")

if st.button("🧾 Generate PDF Summary"):
    st.warning("🔧 PDF feature coming in next update!")

st.caption("Built with ❤️ using Streamlit + Lottie")
