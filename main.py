import streamlit as st
import upload_gds
import adjuster_questions
import rrt_zap
import final_demand
import escalation

# Set the page layout
st.set_page_config(page_title="Genesis Guided Demo", layout="wide")

# 🧠 DEBUG: Print current session state on every launch
st.write("🧠 SESSION STATE AT LAUNCH:", dict(st.session_state))

# 🔄 Initialize session state only if missing
if "page" not in st.session_state:
    st.session_state["page"] = "upload"
if "claim_data" not in st.session_state:
    st.session_state["claim_data"] = None
if "adjuster_profile" not in st.session_state:
    st.session_state["adjuster_profile"] = None
if "adjuster_summary" not in st.session_state:
    st.session_state["adjuster_summary"] = {}

# Mapping of sections to the functions to be called
PAGES = {
    "upload": upload_gds.show,
    "adjuster": adjuster_questions.show,
    "rrt": rrt_zap.show,
    "final_demand": final_demand.show,
    "escalation": escalation.show
}

# Display page based on current session state["page"]
def navigate_to_next_page():
    if st.session_state["page"] == "upload":
        st.session_state["page"] = "adjuster"
    elif st.session_state["page"] == "adjuster":
        st.session_state["page"] = "rrt"
    elif st.session_state["page"] == "rrt":
        st.session_state["page"] = "final_demand"
    elif st.session_state["page"] == "final_demand":
        st.session_state["page"] = "escalation"

def show_current_page():
    page = st.session_state["page"]
    PAGES[page]()

# Start with the current page
show_current_page()

# Add the "Next" button at the bottom of each page
if st.session_state["page"] != "escalation":  # Prevent showing next button on last page
    if st.button("Next ➡️"):
        navigate_to_next_page()
        st.experimental_rerun()
