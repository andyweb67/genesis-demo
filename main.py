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

# 🔀 Mapping of pages to display functions
PAGES = {
    "upload": upload_gds.show,
    "adjuster": adjuster_questions.show,
    "rrt": rrt_zap.show,
    "final_demand": final_demand.show,
    "escalation": escalation.show
}

# 🔁 Navigate forward in order
def navigate_to_next_page():
    page_order = list(PAGES.keys())
    current = st.session_state["page"]
    if current in page_order:
        idx = page_order.index(current)
        if idx + 1 < len(page_order):
            st.session_state["page"] = page_order[idx + 1]

# 🔁 Show current page
def show_current_page():
    page = st.session_state["page"]
    PAGES[page]()

# 🚦 Display the current module/page
show_current_page()

# 📍 Helper for Section 1 (upload) if no claim data yet
if st.session_state["page"] == "upload" and not st.session_state.get("claim_data"):
    st.info("Please upload your extracted_demand.json or simulate upload to continue.")

# ⏭️ Next button only if valid to proceed
if st.session_state["page"] != "escalation":
    # Don't allow Next on upload page unless claim_data is set
    if st.session_state["page"] != "upload" or st.session_state.get("claim_data"):
        if st.button("Next ➡️"):
            navigate_to_next_page()
            st.experimental_rerun()
