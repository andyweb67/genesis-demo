# 5_escalation.py

import streamlit as st
import datetime

# 🚨 Confirm escalation.py is running as the main app
st.title("🚨 This is escalation.py running as main")
st.stop()

st.title("Section 5 – Adjuster Non-Compliance Escalation")

if 'claim_data' not in st.session_state or 'adjuster_summary' not in st.session_state:
    st.warning("Missing data from previous sections. Please complete Sections 1–4 first.")
    st.stop()

claim = st.session_state.claim_data
adjuster = st.session_state.adjuster_summary
claim_number = claim.get('claim_number', 'GEN-00000')
claimant_name = claim.get('claimant_name', 'Claimant')
adjuster_name = claim.get('adjuster', 'the assigned adjuster')

# -----------------------------
# Phone Call Script Simulation
# -----------------------------

st.subheader("📞 Phone Call Script: Final Escalation Attempt")
st.markdown(f"""
**Estimated Call Time:** 5–7 Minutes

**Opening Statement:**
"Hello, {adjuster_name}. This is [Your Name] from [Your Firm]. I’m following up on Claim #{claim_number}. You have already received the Reconciliation Review Table (RRT) and previous notices regarding valuation concerns. This is a final notice before escalation."
""")

st.markdown("---")
st.markdown("""
**Quick Assessment of Adjuster Justifications:**

- ✅ Medical Specials Adjustment: *Genesis flagged unjustified reduction.*
- ✅ IME Ordered: *None conducted, treating physician remains primary source.*
- ✅ Pain & Suffering: *AI suppression detected; valuation is below jurisdictional standards.*
""")

st.markdown("---")
st.markdown("""
**Prophet Simulation Reminder:**
"Prophet projects an 80% success rate at trial, with a likely jury award of $150,000—significantly higher than your offer."
"Your defense model will be forced to use the same data. Are you escalating or risking discovery of your valuation methods during litigation?"
""")

st.markdown("---")
st.markdown("""
**Final Action Request:**
"The litigation model favors the Plaintiff. Are you escalating this to your supervisor?"
"If a revised offer is not provided within 7 business days, we will escalate to litigation and UFCPA regulatory review."
""")

# ------------------------
# Post-Call Escalation Step
# ------------------------

escalate = st.radio("Did the adjuster agree to escalate the claim internally?", [
    "No – No revised offer received",
    "Yes – Offer pending or escalation acknowledged"
])

if escalate == "No – No revised offer received":
    st.subheader("📧 Escalation Email Preview")
    st.markdown(f"""
    **Subject:** Updated Valuation Simulation for Claim #{claim_number} – {claimant_name}  
    **From:** responses@PM.abclawfirm.com

    GEICO's prior offer has been reviewed. Following your failure to provide revised justification or escalate the matter after live contact, PlaintiffMax has issued the enclosed litigation simulation.

    This report outlines projected jury valuation based on current claim facts, jurisdictional verdict history, and statutory obligations. We strongly recommend internal review by claim management or defense counsel.

    📎 [Download Prophet Report PDF]

    This notice serves as a pre-litigation risk disclosure and will be preserved for regulatory and court record purposes.
    """)
    st.success("✅ UFCPA Escalation Option locked in. You may now archive this claim as escalated.")

else:
    st.info("Adjuster has agreed to escalate internally. No further action required at this time.")

st.markdown("---")
st.caption("Genesis – Section 5 complete. Claim status can now be updated or archived.")
