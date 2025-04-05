import streamlit as st
import datetime

def show():
    st.title("Step 4 – Final Demand & Prophet Simulation")

    if 'claim_data' not in st.session_state or 'adjuster_summary' not in st.session_state:
        st.warning("Missing prior section data. Please complete Sections 1–3 first.")
        return

    claim = st.session_state.claim_data
    adjuster = st.session_state.adjuster_summary

    st.markdown("""
    ### \U0001F4CB Adjuster Summary Recap
    Genesis has completed its audit. The adjuster is aware of the analysis and continues to support cost-containment measures inconsistent with fiduciary obligations.

    Should you authorize escalation, Prophet will initiate pre-litigation protocols, simulate court risk, and prepare documentation for regulatory action.
    """)

    att_demand_total = claim['gds_table']['total']['attorney']
    jurisdiction_multiplier = 4.482
    genesis_medicals = float(claim['gds_table']['medical_specials_total']['genesis'])

    projected_pns = round(jurisdiction_multiplier * genesis_medicals, 2)
    projected_econ = float(claim['gds_table']['lost_wages']['attorney']) + float(claim['gds_table']['future_medicals']['attorney'])
    projected_total = round(projected_pns + projected_econ, 2)

    decision = st.radio("How would you like to proceed?", [
        "✅ Authorize Final Demand & Pre-Litigation Notice",
        "🔁 Request Further Adjuster Revisions",
        "❌ Cancel – No Action Now"
    ])

    if decision == "✅ Authorize Final Demand & Pre-Litigation Notice":
        st.success("Final Demand Letter and Prophet Summary are now generated.")

        st.subheader("\U0001F4C4 Final Demand Letter Preview")
        st.markdown(f"""
**Date:** {datetime.date.today().strftime('%B %d, %Y')}  
**Claimant:** {claim['claimant_name']}  
**Claim Number:** {claim['claim_number']}  
**Adjuster:** {claim.get('adjuster', 'N/A')}  
**Carrier:** GEICO

---

This letter serves as our formal Final Demand before initiating litigation. Genesis identified discrepancies in your evaluation that conflict with regulatory standards and fiduciary obligations.

**Key Findings:**
- Claim IQ valuation denial contradicted by internal offer data
- Medical Specials adjusted without IME → ⚠ Improper suppression
- Pain & Suffering value (${adjuster.get('pain_and_suffering', '0')}) falls below historical average (${projected_pns})
- Lost Wages or Future Medicals excluded without explanation

---

### ⚖️ Required Action
- Immediate reevaluation of your offer using fair benchmarks
- Written justification for all disputed reductions
- Confirmation of final settlement position within 7 days

Failure to comply will result in:
- Filing of regulatory complaints for bad faith
- Formal litigation seeking excess liability
- Discovery of all internal valuation models used

Sincerely,  
[Attorney Name]  
[Law Firm Name]  
[Contact Info]
        """)

        st.subheader("\U0001F4CA Prophet Litigation Simulation")
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

    st.markdown("✅ Section 4 complete. Click **Next** to proceed to the Escalation step.")
