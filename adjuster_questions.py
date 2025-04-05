import streamlit as st

st.title("Section 2 – Adjuster Questions")

# Load claim data
if 'claim_data' not in st.session_state or not st.session_state.claim_data:
    st.warning("No claim data found. Please complete Section 1 first.")
    st.stop()

if 'adjuster_profile' not in st.session_state:
    st.error("Adjuster profile not assigned. Please return to Home and begin demo properly.")
    st.stop()

claim = st.session_state.claim_data
summary = {}

profile = st.session_state.adjuster_profile

# Profiles
predefined_profiles = {
    "Fair Adjuster (Cooperative)": {
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
    },
    "Tough Adjuster (Resistant)": {
        "adjuster_name": "Brandon Brick",
        "adjuster_email": "brandonbrick@geicoclaims.com",
        "initial_offer": 27000,
        "claim_type": "Third Party",
        "liability_acknowledgment": "Yes – I acknowledge this determination",
        "ime_ordered": "No",
        "claim_software": "No – We use our experience",
        "medical_specials_eval": [
            {"provider": "Exacta Care", "adjuster_eval": "2500", "justification": "Reduced – treatment seemed excessive"},
            {"provider": "Real Chiropractic", "adjuster_eval": "5500", "justification": "Reduced slightly"},
            {"provider": "Cannon Memorial Hospital", "adjuster_eval": "2000", "justification": "Accepted as billed"}
        ],
        "pain_and_suffering": "15000",
        "future_medicals": "0",
        "lost_wages": "2000",
        "mileage": "0",
        "subtotal": "27000",
        "final_dispute": "Yes",
        "dispute_notes": "Some treatment bills were excessive"
    },
    "Aggressive Adjuster (Non-Compliant)": {
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
}

profile_data = predefined_profiles.get(profile, {})

st.markdown(f"### 👤 Assigned Adjuster: **{profile}**")

# Acknowledgment
st.markdown("### ⚖️ Acknowledgment of First-Party Duty")
summary['first_party_acknowledgment'] = "No – I am treating this as a third-party claim"

# Step 1: Liability
st.markdown("### 📌 Step 1: Liability Confirmation")
causation = claim.get("liability_determination", "[Causation summary missing]")
st.markdown(f"> Causation Summary: *\"{causation}\"*")
summary['liability_acknowledgment'] = profile_data['liability_acknowledgment']
if profile_data['liability_acknowledgment'].startswith("No"):
    summary['liability_dispute'] = profile_data.get('liability_dispute', "")

# Step 2: IME
st.markdown("### Step 2: Independent Medical Examination (IME)")
summary['ime_ordered'] = profile_data['ime_ordered']

# Step 3: Software
st.markdown("### Step 3: Valuation Software Disclosure")
summary['claim_software'] = profile_data['claim_software']

# Step 4: Medical Specials
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

# Step 5: Pain & Suffering
st.markdown("### Step 5: Pain & Suffering")
summary['pain_and_suffering'] = profile_data['pain_and_suffering']

# Step 6: Additional Disputes
st.markdown("### Step 6: Additional Comments")
summary['final_dispute'] = profile_data['final_dispute']
summary['dispute_notes'] = profile_data['dispute_notes']

# Save
st.success(f"✅ Adjuster responses recorded for: {profile}")
st.session_state.adjuster_summary = summary

st.subheader("📋 Adjuster Summary Preview")
st.json(summary)

st.markdown("You may now proceed to Section 3: Reconciliation Review Table (RRT).")
