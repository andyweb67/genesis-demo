# 2_Adjuster_Questions.py

import streamlit as st
import json

st.title("Section 2 – Adjuster Questions")

# Load claim data
if 'claim_data' not in st.session_state or not st.session_state.claim_data:
    st.warning("No claim data found. Please complete Section 1 first.")
    st.stop()

claim = st.session_state.claim_data
summary = {}

# Profile dropdown
st.markdown("### 🔄 Adjuster Profile Simulation")
profile_choice = st.selectbox("Select Demo Adjuster Profile", ["Manual Entry", "Fair Adjuster"])

# Predefined profile values
predefined_profiles = {
    "Fair Adjuster": {
        "adjuster_name": "Mary Jones",
        "adjuster_email": "maryjones@geicoclaims.com",
        "initial_offer": 36250,
        "claim_type": "Third Party",
        "liability_acknowledgment": "Yes – I acknowledge this determination",
        "ime_ordered": "No",
        "claim_software": "Yes – Claim IQ",
        "medical_specials_eval": [
            {"provider": "Exacta Care", "adjuster_eval": "5000", "justification": "Accepted in full"},
            {"provider": "Real Chiropractic", "adjuster_eval": "7000", "justification": "Accepted in full"},
            {"provider": "Cannon Memorial Hospital", "adjuster_eval": "3000", "justification": "Accepted in full"}
        ],
        "pain_and_suffering": "18750",
        "future_medicals": "0",
        "lost_wages": "2500",
        "mileage": "0",
        "subtotal": "36250",
        "final_dispute": "No",
        "dispute_notes": ""
    }
}

# Load profile data
profile_data = predefined_profiles.get(profile_choice, {})

# First-party Acknowledgment
st.markdown("### ⚖️ Acknowledgment of First-Party Duty")
first_party_ack = st.radio(
    "Do you acknowledge this heightened duty of fair claim evaluation?",
    ["Yes – I acknowledge fiduciary obligations", "No – I am treating this as a third-party claim"],
    index=0
)
summary['first_party_acknowledgment'] = first_party_ack

# Liability Confirmation
st.markdown("### 📌 Step 1: Liability Confirmation")
causation = claim.get("liability_determination", "[Causation text missing from police report.]")
st.markdown(f"> Causation Summary: *\"{causation}\"*")

liability_choice = st.radio(
    "Do you accept the liability determination?",
    ["Yes – I acknowledge this determination", "No – I dispute this determination"],
    index=0 if profile_data.get("liability_acknowledgment", "Yes") == "Yes – I acknowledge this determination" else 1
)
summary['liability_acknowledgment'] = liability_choice
if liability_choice == "No – I dispute this determination":
    summary['liability_dispute'] = st.text_area("Provide written justification:")

# Step 2: IME Ordered
st.markdown("### Step 2: Independent Medical Examination (IME)")
ime_ordered = st.radio("Was an IME ordered?", ["Yes", "No"], index=1 if profile_data.get("ime_ordered") == "No" else 0)
summary['ime_ordered'] = ime_ordered

# Step 3: Software Usage
st.markdown("### Step 3: Valuation Software Disclosure")
software_used = st.radio("Was Claim IQ or other software used?", ["Yes", "No"], index=0 if profile_data.get("claim_software") == "Yes – Claim IQ" else 1)
summary['claim_software'] = software_used

# Step 4: Medical Specials Evaluation
st.markdown("### Step 4: Medical Specials Evaluation")
med_specials = []
for provider in claim['gds_table']['providers']:
    provider_name = provider['name']
    p_data = next((p for p in profile_data.get("medical_specials_eval", []) if p['provider'] == provider_name), {})
    col1, col2 = st.columns([3, 2])
    with col1:
        adj_val = st.text_input(f"{provider_name} – Genesis Billed: ${provider['genesis']}", value=p_data.get("adjuster_eval", ""))
    with col2:
        justification = st.text_input(f"Justification", value=p_data.get("justification", ""), key=f"justification_{provider_name}")
    med_specials.append({
        "provider": provider_name,
        "genesis": provider['genesis'],
        "adjuster_eval": adj_val,
        "justification": justification
    })
summary['medical_specials_eval'] = med_specials

# Step 5: Pain & Suffering
st.markdown("### Step 5: Pain & Suffering")
pns_value = st.text_input("What is your evaluated Pain & Suffering amount?", value=profile_data.get("pain_and_suffering", ""))
summary['pain_and_suffering'] = pns_value

# Step 6: Additional Disputes
st.markdown("### Step 6: Additional Comments")
final_dispute = st.radio("Any further objections?", ["No", "Yes"], index=0 if profile_data.get("final_dispute") == "No" else 1)
summary['final_dispute'] = final_dispute
if final_dispute == "Yes":
    summary['dispute_notes'] = st.text_area("Please describe your additional dispute(s):", value=profile_data.get("dispute_notes", ""))

# Save response
display_name = profile_choice if profile_choice != "Manual Entry" else "Manual Adjuster"
st.success(f"✅ Adjuster responses recorded for: {display_name}")
st.session_state.adjuster_summary = summary

st.subheader("📋 Adjuster Summary Preview")
st.json(summary)

st.markdown("You may now proceed to Section 3: Reconciliation Review Table (RRT).")
