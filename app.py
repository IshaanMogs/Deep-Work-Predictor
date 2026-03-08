import streamlit as st
import requests
import boto3
import pandas as pd
import re

# -----------------------------
# CONFIG
# -----------------------------

API_URL = "https://0xyqw1cb77.execute-api.us-east-1.amazonaws.com/default/Deepwork-Orchestrator"

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("UserProductivityTable")


# -----------------------------
# PAGE SETUP
# -----------------------------

st.set_page_config(
    page_title="Cognitive Productivity AI",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI Productivity Coach")
st.write("Enter your cognitive vitals to generate a personalized productivity plan.")

# -----------------------------
# DASHBOARD LAYOUT
# -----------------------------

col1, col2 = st.columns([1,1])

# -----------------------------
# INPUT PANEL
# -----------------------------

with col1:

    st.subheader("Vitals")

    sleep = st.slider("Sleep Hours", 0, 10, 7)
    exercise = st.slider("Exercise Minutes", 0, 60, 20)
    stress = st.slider("Stress Level", 1, 10, 4)
    noise = st.slider("Noise Level", 0, 80, 40)

    goal = st.text_input("Study Goal", "Master DSA Recursion")

    generate = st.button("Generate Plan")

# -----------------------------
# RESULT PANEL
# -----------------------------

with col2:

    if generate:

        payload = {
            "user_id": "student_19",
            "goal": goal,
            "vitals": [sleep, exercise, stress, noise]
        }

        try:

            response = requests.post(API_URL, json=payload)
            result = response.json()

            focus_score = result["focus_score"]
            decision = result["decision"]
            roadmap = result["personalized_roadmap"]

            # -----------------------------
            # CLEAN MODEL OUTPUT
            # -----------------------------

            roadmap = roadmap.replace("Here is the output:", "")
            roadmap = roadmap.replace("```", "")
            roadmap = roadmap.replace("python", "")

            if "Deep Work Execution Plan" in roadmap:
                roadmap = roadmap.split("Deep Work Execution Plan")[0]

            if "END OF DEEP WORK EXECUTION PLAN" in roadmap:
                roadmap = roadmap.split("END OF DEEP WORK EXECUTION PLAN")[0]

            roadmap = roadmap.strip()

            # -----------------------------
            # FOCUS SCORE
            # -----------------------------

            st.subheader("Focus Score")

            st.metric("Score", focus_score)
            st.progress(focus_score / 100)

            # -----------------------------
            # DECISION
            # -----------------------------

            st.subheader("Decision")

            if decision == "FOCUS NOW":
                st.success("⚡ Focus Mode Activated")
            else:
                st.warning("🧘 Recovery Mode Recommended")

            # -----------------------------
            # EXECUTION PLAN
            # -----------------------------

            st.subheader("Execution Plan")

            steps = re.split(r"Step\s*\d+", roadmap)
            step_numbers = re.findall(r"Step\s*\d+", roadmap)

            for i, step in enumerate(steps):

                if step.strip():

                    step_title = step_numbers[i] if i < len(step_numbers) else f"Step {i+1}"

                    st.markdown(
                        f"""
                        <div style="
                        background:#111;
                        padding:20px;
                        border-radius:12px;
                        margin-bottom:12px;
                        border:1px solid #333;
                        ">
                        <h4>{step_title}</h4>
                        <p>{step.strip()}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        except Exception as e:
            st.error(f"API Error: {e}")


# -----------------------------
# SESSION HISTORY
# -----------------------------

st.divider()
st.subheader("Session History")

try:

    response = table.scan()
    items = response.get("Items", [])

    if items:

        df = pd.DataFrame(items)

        df = df.sort_values("timestamp", ascending=False)

        df = df[["goal", "focus_score", "decision"]]

        st.dataframe(df, use_container_width=True)

    else:
        st.write("No sessions recorded yet.")

except Exception as e:

    st.error(f"Error loading history: {e}")
