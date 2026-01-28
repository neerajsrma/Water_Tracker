import streamlit as st
from datetime import datetime
import pandas as pd
from src.agent import WaterIntakeAgent
from src.database import log_intake, get_intake_history

if "tracker_started" not in st.session_state:
    st.session_state.tracker_started = False

if not st.session_state.tracker_started:
    st.title("Welcome to Smart Water Tracker")
    st.markdown("""
    Track your daily hydration with the help of AI Assistant.
    Log your intake, get smart feedback and stay healthy effortlessly
    
    """)

    if st.button("Start Tracking"):
        st.session_state.tracker_started = True
        st.expermental_rerun()

else:
    st.title("AI Water Tracker DashBoard")

    # sidebar : Intake Input
    st.sidebar.header("Log your water intake")
    user_id = st.sidebar.text_input("User ID",value="Mansi01")
    intake_ml = st.sidebar.number_input("Water Intake (ml)", min_value=0, step=100)

    if st.sidebar.button("Submit"):
        if user_id and intake_ml:
            log_intake(user_id, intake_ml)
            st.success(f"Logged {intake_ml} for {user_id}")

            agent = WaterIntakeAgent()
            feedback = agent.analyze_intake(intake_ml)
            st.info(f"AI feedback : {feedback}")

    # Divider
    st.markdown("--------------")

    # History Section
    st.header("Water Intake History")
    if user_id:
        history = get_intake_history(user_id)
        if history:
            dates = [datetime.strptime(row[1], "%Y-%m-%d") for row in history]
            values = [row[0] for row in history]

            df = pd.DataFrame({
                "Date":dates,
                "Water Intake (ml)":values
            })

            st.dataframe(df)
            st.line_chart(df, x="Date", y="Water Intake (ml)")
        else:
            st.warning("No water intake data found. Please log your intake first")