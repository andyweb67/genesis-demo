# pages/adjuster_questions.py

import streamlit as st

def show():
    st.title("Step 2 – Adjuster Questions")

    if 'claim_data' not in st.session_state or not st.session_state.claim_data:
        st.warning("No claim data found. Please complete Section 1 first.")
        return

    if 'adjuster_profile' not in st.session_state:
        st.warning("Adjuster profile not assigned. Please return to upload.")
        return

    claim = st.session_state.claim_data
    profile = st.session_state.adjuster_profile
    summary = {}

    # Predefined profiles (trimmed for clarity here)
    from utils.adjuster_profiles import predefined_profiles
    profile_data = predefined_profiles.get(profile, {})

    st.markdown(f"### 👤 Assigned Adjuster: **{profile}**")

    summary['liability_acknowledgment'] = profile_data.get("liability_acknowledgment", "N/A")
    summary['ime_ordered'] = profile_data.get("ime_ordered", "N/A")
    summary['claim_software'] = profile_data.get("claim_software", "N/A")
    summary['pain_and_suffering'] = profile_data.get("pain_and_suffering", "0")
    summary['final_dispute'] = profile_data.get("final_dispute", "No")
    summary['dispute_notes'] = profile_data.get("dispute_notes", "")

    med_specials = []
    for provider in claim['gds_table']['providers']:
        match = next((p for p in profile_data['medical_specials_eval'] if p['provider'] == provider['name']), {})
        med_specials.append({
            "provider": provider['name'],
            "genesis": provider['genesis'],
            "adjuster_eval": match.get('adjuster_eval', "0"),
            "justification": match.get('justification', "")
        })
    summary['medical_specials_eval'] = med_specials

    st.success("✅ Adjuster responses recorded.")
    st.session_state.adjuster_summary = summary
    st.json(summary)

    st.markdown("✅ Section 2 complete. Click **Next** to proceed to the Reconciliation Table.")
