import streamlit as st

# Import each section as a module
import 1_Upload_and_GDS as upload_gds
import 2_Adjuster_Questions as adjuster_questions
import 3_RRT_and_Zap as rrt_zap
import 4_Final_Demand_Prophet as final_demand
import 5_Human_Intervention as escalation

st.set_page_config(page_title="Genesis Guided Demo", layout="wide")

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "upload"

# Optional: adjuster profile randomization (set once)
if "adjuster_profile" not in st.session_state:
    import random
    st.session_state.adjuster_profile = random.choice([
        "Fair Adjuster (Cooperative)",
        "Tough Adjuster (Resistant)",
        "Aggressive Adjuster (Non-Compliant)"
    ])

# Header (Persistent)
st.title("Genesis MVP: Guided Claim Audit")
st.markdown(f"**Step:** {st.session_state.page.replace('_', ' ').title()}")

# Page router
if st.session_state.page == "upload":
    upload_gds.show()

elif st.session_state.page == "adjuster":
    adjuster_questions.show()

elif st.session_state.page == "rrt":
    rrt_zap.show()

elif st.session_state.page == "final":
    final_demand.show()

elif st.session_state.page == "escalation":
    escalation.show()

# Navigation (Optional)
st.sidebar.title("Navigation")
st.sidebar.write("Guided navigation through Genesis modules")
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Restart Demo"):
    st.session_state.clear()
    st.experimental_rerun()
