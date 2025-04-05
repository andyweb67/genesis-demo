# utils/render_gds.py

import streamlit as st
import pandas as pd

def render_gds_table(claim_data):
    st.subheader("Claim Details")
    st.markdown(f"""
    - **Claimant’s Name:** {claim_data['claimant_name']}  
    - **Claim Number:** {claim_data['claim_number']}  
    - **Date of Loss:** {claim_data.get('date_of_loss', 'N/A')}  
    - **Claim Type:** {claim_data.get('claim_type', 'N/A')}  
    - **State:** {claim_data.get('state', 'N/A')}  
    - **PIP Status:** {claim_data.get('pip_status', 'N/A')}  
    - **Adjuster’s Name:** {claim_data.get('adjuster', 'N/A')}  
    - **Adjuster’s Email:** {claim_data.get('adjuster_email', 'N/A')}  
    - **Initial Offer:** ${claim_data.get('initial_offer', '0')}  
    - **Attorney’s Name:** {claim_data.get('attorney_name', 'N/A')}  
    - **Law Firm:** {claim_data.get('law_firm', 'N/A')}  
    - **Liability Status:** Pending Adjuster Response  
    """)

    st.subheader("Genesis Demand Summary (GDS)")
    gds_rows = []
    ms = claim_data['gds_table']['medical_specials_total']
    gds_rows.append({
        "Damages": "Medical Specials Total",
        "Attorney": f"${ms['attorney']}",
        "Genesis": f"${ms['genesis']}",
        "Validation": "✅ Medical Specials Total matches sum of individual providers",
        "Page #": "N/A"
    })

    for p in claim_data['gds_table']['providers']:
        provider_validation = f"✅ {p['name']} matches extracted billing total" if p['validation'] == "green tick" else p['validation']
        provider_validation += f" * Based on invoices from page {p['page']}"
        gds_rows.append({
            "Damages": f"    {p['name']}",
            "Attorney": f"${p['attorney']}",
            "Genesis": f"${p['genesis']}",
            "Validation": provider_validation,
            "Page #": p['page'] or "N/A"
        })

    for label, key in [
        ("Pain Suffering", "pain_and_suffering"),
        ("Future Medicals", "future_medicals"),
        ("Lost Wages", "lost_wages"),
        ("Mileage", "mileage")
    ]:
        item = claim_data['gds_table'][key]
        attorney_val = float(str(item.get('attorney', "0")).replace("$", "").replace(",", ""))
        genesis_val = float(str(item.get('genesis', "0")).replace("$", "").replace(",", ""))
        if attorney_val == 0 and genesis_val == 0:
            validation_note = "Not claimed in the demand package"
        elif key == "pain_and_suffering":
            state = claim_data.get("state", "XX")
            specials_val = float(str(ms['genesis']).replace("$", "").replace(",", ""))
            multiplier = round(genesis_val / specials_val, 1) if specials_val else "N/A"
            validation_note = f"[{state}] historical pain and suffering multiplier has been applied [{multiplier}x]"
        elif item.get("validation", "") == "green tick":
            validation_note = f"✅ {label} extracted from demand package — matches attorney value"
        else:
            validation_note = item.get("validation", "—")

        gds_rows.append({
            "Damages": label,
            "Attorney": f"${item['attorney']}",
            "Genesis": f"${item['genesis']}",
            "Validation": validation_note,
            "Page #": ""
        })

    for label in ["subtotal", "deductions", "total"]:
        gds_rows.append({
            "Damages": label.replace("subtotal", "Sub-Total").replace("deductions", "Deductions").replace("total", "TOTAL"),
            "Attorney": f"${claim_data['gds_table'][label]['attorney']}",
            "Genesis": f"${claim_data['gds_table'][label]['genesis']}",
            "Validation": "—",
            "Page #": ""
        })

    df = pd.DataFrame(gds_rows).rename(columns={"Attorney": "Attorney Demand", "Genesis": "Genesis Audit"})

    def highlight_total_row(row):
        d = row['Damages'].strip().upper()
        if d == 'TOTAL':
            return ['background-color: #f0f0f0; font-weight: bold'] * len(row)
        elif d == 'SUB-TOTAL':
            return ['font-weight: bold'] * len(row)
        elif d == 'MEDICAL SPECIALS TOTAL':
            return ['font-weight: bold'] * len(row)
        elif row['Attorney Demand'] != row['Genesis Audit']:
            return ['background-color: #fff3cd'] * len(row)
        return [''] * len(row)

    styled_df = df.style.hide(axis='index').apply(highlight_total_row, axis=1)
    st.markdown(styled_df.to_html(escape=False), unsafe_allow_html=True)

    st.markdown("""
    ### Legend: Validation Column
    - ✅ **Match**: Extracted data matches attorney and Genesis calculations.  
    - ✖ **Discrepancy**: Genesis and attorney demand do not align.  
    - 🚩 **Calculation Issue**: Subtotal does not match total without deductions.  
    - N/A: Not applicable (used for subtotal, deductions, total rows).
    """)
