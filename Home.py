import streamlit as st
import random

st.set_page_config(page_title="Genesis MVP - Home", layout="centered")

st.title("🧠 Genesis MVP – Claims Audit Demonstration")
st.subheader("Select Adjuster Path (Randomized)")

# Random Adjuster Selection (simulate real-world assignment)
adjuster_options = {
    "Fair Adjuster (Cooperative)": "2_Adjuster_Questions_Fair",
    "Tough Adjuster (Resistant)": "2_Adjuster_Questions_Tough",
    "Aggressive Adjuster (Non-Compliant)": "2_Adjuster_Questions_Aggressive"
}

if "adjuster_profile" not in st.session_state:
    st.session_state.adjuster_profile = random.choice(list(adjuster_options.keys()))
    st.session_state.adjuster_file = adjuster_options[st.session_state.adjuster_profile]

st.markdown("---")
st.subheader("🚀 Instructions")
st.markdown(f"""
Genesis has randomly assigned you to an adjuster profile — just like in the real world:

**Assigned Adjuster:** `{st.session_state.adjuster_profile}`  
**Loaded File:** `{st.session_state.adjuster_file}.py`

1. Click **'Begin Demo'** to open Section 1 (Upload & GDS).  
2. Use the **sidebar to navigate manually** between sections (1 to 5).  
3. Section 2 will automatically use your assigned adjuster model.
""")

if st.button("▶ Begin Demo (Start at Section 1)"):
    st.switch_page("pages/1_Upload_and_GDS.py")
