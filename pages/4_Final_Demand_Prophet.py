# 4_Final_Demand_Prophet.py

import streamlit as st
import datetime

st.title("Section 4 – Final Demand & Prophet Simulation")

# Check dependencies
if 'claim_data' not in st.session_state or 'adjuster_summary' not in st.session_state:
    st.warning("Missing prior section data. Please complete Sections 1–3 first.")
    st.stop()

claim = st.session_state.claim_data
adjuster = st.session_state.adjuster_summary

# --------------------------
# Section 4 – Summary Review
# --------------------------

st.markdown("""
### 📋 Adjuster Summary Recap
Genesis has completed its audit. The adjuster is aware of the analysis and continues to support cost-containment measures inconsistent with fiduciary obligations.

Should you authorize escalation, Prophet will initiate pre-litigation protocols, simulate court risk, and prepare documentation for regulatory action. Your approval is required to proceed.
""")

att_demand_total = claim['gds_table']['total']['attorney']
adjuster_offer = claim.get("adjuster_offer", 21500)  # Default mock offer
jurisdiction_multiplier = 4.482
genesis_medicals = float(claim['gds_table']['medical_specials_total']['genesis'])

# Prophet Simulation Logic
projected_pns = round(jurisdiction_multiplier * genesis_medicals, 2)
projected_econ = float(claim['gds_table']['lost_wages']['attorney']) + float(claim['gds_table']['future_medicals']['attorney'])
projected_total = round(projected_pns + projected_econ, 2)

# ------------------------------------
# Decision Trigger: Attorney Options
# ------------------------------------

decision = st.radio("How would you like to proceed?", [
    "✅ Authorize Final Demand & Pre-Litigation Notice",
    "🔁 Request Further Adjuster Revisions",
    "❌ Cancel – No Action Now"
])

# If Authorized, Show Generated Content
if decision == "✅ Authorize Final Demand & Pre-Litigation Notice":
    st.success("Final Demand Letter and Prophet Summary are now generated.")

    st.subheader("📄 Final Demand Letter Preview")
    st.markdown(f"""
**Date:** {datetime.date.today().strftime('%B %d, %Y')}  
**Claimant:** {claim['claimant_name']}  
**Claim Number:** {claim['claim_number']}  
**Adjuster:** {claim.get('adjuster', 'N/A')}  
**Carrier:** GEICO  

---

Dear {claim.get('adjuster', 'Claims Adjuster')},

This letter serves as our formal Final Demand before initiating litigation. Genesis identified discrepancies in your evaluation that conflict with regulatory standards and fiduciary obligations.

**Key Findings:**
- Claim IQ valuation denial contradicted by internal offer data
- Medical Specials adjusted without IME → ⚠ Improper suppression
- Pain & Suffering value (${adjuster.get('pain_and_suffering', '0')}) falls below historical average (${projected_pns})
- Potential WPI value omission (if applicable)
- Lost Wages, Mileage, or Future Medicals excluded without explanation

---

### ⚖️ Required Action
- Immediate reevaluation of your offer using fair benchmarks
- Written justification for all disputed reductions
- Confirmation of final settlement position within 7 days

---

Failure to comply will result in:
- Filing of regulatory complaints for bad faith
- Formal litigation seeking excess liability
- Discovery of all internal valuation models used

We urge GEICO to reconsider its position to avoid avoidable exposure.

Sincerely,  
[Attorney Name]  
[Law Firm Name]  
[Contact Info]
""")

    st.subheader("📊 Prophet Litigation Simulation")
    st.markdown(f"""
- **Jurisdictional Multiplier Used:** {jurisdiction_multiplier}x
- **Projected Pain & Suffering Award:** ${projected_pns:,.2f}  
- **Projected Economic Losses:** ${projected_econ:,.2f}  
- **Total Estimated Verdict:** ${projected_total:,.2f}  
- **Bad Faith Risk Level:** Very High ⚠
""")

elif decision == "🔁 Request Further Adjuster Revisions":
    st.info("Adjuster will be prompted to revise their offer and resubmit justifications.")

elif decision == "❌ Cancel – No Action Now":
    st.warning("No action taken. You may revisit this decision anytime.")
