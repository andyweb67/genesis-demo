# pages/upload_gds.py

import streamlit as st
import pandas as pd
import os
import json
import time

def show():
    st.title("Step 1 – Upload & Genesis Demand Summary (GDS)")

    if 'claim_data' not in st.session_state:
        st.session_state.claim_data = None

    st.markdown("""
    > **Opening Statement to Adjusters:**  
    > This Genesis audit highlights undervaluation of the claim and enforces accountability. The claimant has provided full transparency through the Genesis Demand Summary (GDS) and supporting documents.
    """)

    col1, col2 = st.columns([2, 1])
    with col1:
        uploaded_file = st.file_uploader("Choose a file to simulate", type=["pdf", "zip", "docx"])
    with col2:
        demo_trigger = st.button("▶ Simulate Upload")

    if uploaded_file or demo_trigger:
        st.info("Genesis is extracting the claim package...")

        parse_steps = [
            "Extracting demand letter...",
            "Parsing medical bills...",
            "Identifying ICD-10 severity codes...",
            "Loading provider invoices...",
            "Populating Genesis Summary..."
        ]
        for step in parse_steps:
            with st.spinner(step):
                time.sleep(1.0)

        st.success("Package successfully extracted.")

        data_folder = "demo_data"
        case_files = [f for f in os.listdir(data_folder) if f.endswith(".json")]
        selected_file = case_files[0] if case_files else None

        if selected_file:
            with open(os.path.join(data_folder, selected_file)) as f:
                st.session_state.claim_data = json.load(f)

            # Assign an adjuster profile randomly
            import random
            adjusters = ["Fair Adjuster (Cooperative)", "Tough Adjuster (Resistant)", "Aggressive Adjuster (Non-Compliant)"]
            st.session_state.adjuster_profile = random.choice(adjusters)
            st.success(f"Assigned Adjuster Profile: **{st.session_state.adjuster_profile}**")

    # Display GDS table if loaded
    if st.session_state.claim_data:
        from utils.render_gds import render_gds_table
        render_gds_table(st.session_state.claim_data)

        st.markdown("✅ Section 1 complete. Click **Next** to proceed to Adjuster Questions.")
