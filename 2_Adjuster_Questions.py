# 2_Adjuster_Questions.py

import streamlit as st
import json

st.title("Section 2 – Adjuster Questions")

# Load claim data from session state
if 'claim_data' not in st.session_state or not st.session_state.claim_data:
    st.warning("No claim data found. Please complete Section 1 first.")
    st.stop()

claim = st.session_state.claim_data
summary = {}

st.markdown("""
### ⚖️ Acknowledgment of First-Party Duty
If this is a **first-party claim**, you must confirm whether you acknowledge your fiduciary duty to the insured.
""")

first_party_ack = st.radio(
    "Do you acknowledge this heightened duty of fair claim evaluation?",
    ["Yes – I acknowledge fiduciary obligations", "No – I am treating this as a third-party claim"]
)
summary['first_party_acknowledgment'] = first_party_ack

if first_party_ack == "No – I am treating this as a third-party claim":
    st.error("⚠ This response will be logged for potential bad faith exposure.")

# Liability Confirmation
st.markdown("""
### 📌 Step 1: Liability Confirmation
Genesis extracted causation language from the police report.
""")

causation = claim.get("liability_determination", "[Causation text missing from police report.]")
st.markdown(f"> Causation Summary: *\"{causation}\"*")

liability_choice = st.radio(
    "Do you accept the liability determination?",
    ["Yes – I acknowledge this determination", "No – I dispute this determination"]
)

if liability_choice == "No – I dispute this determination":
    justification = st.text_area("Provide written justification and supporting documentation:")
    summary['liability_dispute'] = justification
else:
    summary['liability_acknowledgment'] = "Accepted"

# Step 2: IME Ordered
st.markdown("### Step 2: Independent Medical Examination (IME)")
ime_ordered = st.radio("Was an IME ordered?", ["Yes", "No"])
summary['ime_ordered'] = ime_ordered

if ime_ordered == "Yes":
    ime_type = st.selectbox("Type of IME assessment:", ["In-Person Assessment", "Remote Assessment (e.g., Telehealth)"])
    summary['ime_type'] = ime_type
else:
    treat_ack = st.radio(
        "Do you acknowledge that the treating physician’s findings remain undisputed?",
        ["Yes – Findings remain undisputed", "No – I attempted to modify findings"]
    )
    summary['physician_findings'] = treat_ack

    if treat_ack == "No – I attempted to modify findings":
        st.file_uploader("Upload medical justification:")

# Step 3: Software Usage
st.markdown("### Step 3: Valuation Software Disclosure")
software_used = st.radio("Was Claim IQ or other insurer AI used to determine valuation?", ["Yes", "No"])
summary['claim_software'] = software_used

# Step 4: Medical Specials Table Input
st.markdown("### Step 4: Medical Specials Evaluation")
if st.checkbox("I have reviewed all medical specials and ICD-10 codes"):
    med_specials = []
    for provider in claim['gds_table']['providers']:
        col1, col2 = st.columns([3, 2])
        with col1:
            adjuster_val = st.text_input(f"{provider['name']} – Genesis Billed: ${provider['genesis']}", key=provider['name'])
        with col2:
            reason = st.text_input(f"Reason for Adjustment (if any)", key=provider['name']+"_reason")
        med_specials.append({
            "provider": provider['name'],
            "genesis": provider['genesis'],
            "adjuster_eval": adjuster_val,
            "justification": reason
        })
    summary['medical_specials_eval'] = med_specials
else:
    st.error("Medical Specials section must be completed before continuing.")

# Step 5: Pain & Suffering
st.markdown("### Step 5: Pain & Suffering")
pns_value = st.text_input("What is your evaluated Pain & Suffering amount?")
summary['pain_and_suffering'] = pns_value

# Final Comments
st.markdown("### Step 11: Additional Comments")
final_dispute = st.radio("Do you have any additional objections?", ["No, I have no further disputes.", "Yes – I have additional disputes."])
summary['final_dispute'] = final_dispute

if final_dispute == "Yes – I have additional disputes.":
    details = st.text_area("List any additional disputes not addressed above:")
    summary['dispute_notes'] = details

# Summary display and save
st.success("✅ Adjuster responses recorded.")
st.session_state.adjuster_summary = summary

st.markdown("---")
st.subheader("📋 Adjuster Summary Preview")
st.json(summary)

st.markdown("You may now proceed to Section 3: Reconciliation Review Table (RRT).")
