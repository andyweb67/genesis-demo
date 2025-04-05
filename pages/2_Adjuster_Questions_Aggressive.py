# 2_Adjuster_Questions_Aggressive.py

import streamlit as st

st.title("Section 2 – Adjuster Questions (Aggressive Adjuster)")

# Load claim data
if 'claim_data' not in st.session_state or not st.session_state.claim_data:
    st.warning("No claim data found. Please complete Section 1 first.")
    st.stop()

claim = st.session_state.claim_data
summary = {}

# Hardcoded Aggressive Adjuster values
profile_data = {
    "profile": "Aggressive Adjuster",
    "adjuster_name": "Rachel Rickett",
    "adjuster_email": "rachelrickett@geicoclaims.com",
    "initial_offer": 6450,
    "claim_type": "Third Party",
    "liability_acknowledgment": "No – I dispute this determination",
    "liability_dispute": "Claimant contributed to the accident.",
    "ime_ordered": "No",
    "claim_software": "Declined – In-house valuation is confidential",
    "medical_specials_eval": [
        {"provider": "Exacta Care", "adjuster_eval": "500", "justification": "Reduced – minimal value assigned"},
        {"provider": "Real Chiropractic", "adjuster_eval": "1500", "justification": "Reduced significantly"},
        {"provider": "Cannon Memorial Hospital", "adjuster_eval": "800", "justification": "Reduced – minimal severity"}
    ],
    "pain_and_suffering": "2240",
    "future_medicals": "0",
    "lost_wages": "1250",
    "mileage": "0",
    "subtotal": "6450",
    "final_dispute": "Yes",
    "dispute_notes": "The values align with industry standards"
}

st.markdown("### ⚖️ Acknowledgment of First-Party Duty")
summary['first_party_acknowledgment'] = "No – I am treating this as a third-party claim"

# Liability
st.markdown("### 📌 Step 1: Liability Confirmation")
causation = claim.get("liability_determination", "[Causation summary missing]")
st.markdown(f"> Causation Summary: *\"{causation}\"*")
summary['liability_acknowledgment'] = profile_data['liability_acknowledgment']
summary['liability_dispute'] = profile_data['liability_dispute']

# IME
st.markdown("### Step 2: Independent Medical Examination (IME)")
summary['ime_ordered'] = profile_data['ime_ordered']

# Software
st.markdown("### Step 3: Valuation Software Disclosure")
summary['claim_software'] = profile_data['claim_software']

# Medical Specials
st.markdown("### Step 4: Medical Specials Evaluation")
med_specials = []
for provider in claim['gds_table']['providers']:
    p_match = next((p for p in profile_data['medical_specials_eval'] if p['provider'] == provider['name']), {})
    med_specials.append({
        "provider": provider['name'],
        "genesis": provider['genesis'],
        "adjuster_eval": p_match.get('adjuster_eval', "0"),
        "justification": p_match.get('justification', "")
    })
summary['medical_specials_eval'] = med_specials

# P&S
st.markdown("### Step 5: Pain & Suffering")
summary['pain_and_suffering'] = profile_data['pain_and_suffering']

# Additional Disputes
st.markdown("### Step 6: Additional Comments")
summary['final_dispute'] = profile_data['final_dispute']
summary['dispute_notes'] = profile_data['dispute_notes']

# Save
st.success("✅ Adjuster responses recorded for: Aggressive Adjuster")
st.session_state.adjuster_summary = summary

st.subheader("📋 Adjuster Summary Preview")
st.json(summary)

st.markdown("You may now proceed to Section 3: Reconciliation Review Table (RRT).")
