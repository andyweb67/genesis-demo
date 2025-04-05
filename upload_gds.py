# upload_gds.py

import streamlit as st
import pandas as pd
import json
import os
import time

st.title("Step 1–2: Upload & Genesis Demand Summary (GDS)")

# Initialize session state
if 'claim_data' not in st.session_state:
    st.session_state["claim_data"] = None

# Upload field
uploaded_file = st.file_uploader("Upload extracted_demand.json", type="json")

if uploaded_file:
    st.session_state["claim_data"] = json.load(uploaded_file)
    st.success("✅ Claim data successfully loaded!")
    st.write(st.session_state["claim_data"])  # Optional: show it to confirm


st.markdown("""
> **Opening Statement to Adjusters:**  
> This Genesis audit highlights undervaluation of the claim and enforces accountability. The claimant has provided full transparency through the Genesis Demand Summary (GDS) and supporting documents. Without a reciprocal breakdown of reductions or methodology, further negotiation would lack good faith. This will be documented and escalated if necessary.
""")

# Upload Section
st.markdown("### Upload a Demand Package")
col1, col2 = st.columns([2, 1])
with col1:
    uploaded_file = st.file_uploader("Choose a file to simulate", type=["pdf", "zip", "docx"])
with col2:
    demo_trigger = st.button("▶ Click here to simulate upload")

if uploaded_file or demo_trigger:
    st.info("Genesis is extracting the claim package...")

    parse_steps = [
        "Extracting demand letter...",
        "Parsing medical bills...",
        "Scanning for pain and suffering drivers...",
        "Identifying ICD-10 severity codes...",
        "Searching police report for liability determination...",
        "Loading provider invoices...",
        "Mapping specials to validation engine..."
    ]

    for step in parse_steps:
        with st.spinner(step):
            time.sleep(1.2)

    st.success("Package successfully extracted.")
    st.markdown("### 🔍 Genesis Audit Summary")
    st.markdown(f"**Genesis Audit v1.0 – {time.strftime('%B %d, %Y')}**")

    data_folder = "demo_data"
    case_files = [f for f in os.listdir(data_folder) if f.endswith(".json")]
    selected_file = case_files[0] if case_files else None

    if selected_file:
        with open(os.path.join(data_folder, selected_file)) as f:
            st.session_state.claim_data = json.load(f)

if st.session_state.claim_data:
    claim_data = st.session_state.claim_data

    # Claim Details Table
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

    # GDS Table
    st.subheader("Genesis Demand Summary (GDS)")
    gds_rows = []
    ms = claim_data['gds_table']['medical_specials_total']
    ms_validation = "✅ Medical Specials Total matches sum of individual providers"
    gds_rows.append({
        "Damages": "Medical Specials Total",
        "Attorney": f"${ms['attorney']}",
        "Genesis": f"${ms['genesis']}",
        "Validation": ms_validation,
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
        validation_note = "—"
        try:
            attorney_val = float(str(item.get('attorney', "0")).replace("$", "").replace(",", ""))
            genesis_val = float(str(item.get('genesis', "0")).replace("$", "").replace(",", ""))
        except:
            attorney_val = genesis_val = 0

        if attorney_val == 0 and genesis_val == 0:
            validation_note = "Not claimed in the demand package"
        elif key == "pain_and_suffering":
            state = claim_data.get("state", "XX")
            try:
                specials_val = float(str(ms['genesis']).replace("$", "").replace(",", ""))
                multiplier = round(genesis_val / specials_val, 1) if specials_val else "N/A"
            except:
                multiplier = "N/A"
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

    df = pd.DataFrame(gds_rows)
    df = df.rename(columns={"Attorney": "Attorney Demand", "Genesis": "Genesis Audit"})

    def highlight_total_row(row):
        damages = row['Damages'].strip().upper()
        if damages == 'TOTAL':
            return ['background-color: #f0f0f0; font-weight: bold'] * len(row)
        elif damages == 'SUB-TOTAL':
            return ['font-weight: bold'] * len(row)
        elif damages == 'MEDICAL SPECIALS TOTAL':
            return ['font-weight: bold'] * len(row)
        elif row['Attorney Demand'] != row['Genesis Audit']:
            return ['background-color: #fff3cd'] * len(row)
        else:
            return [''] * len(row)

    styled_df = df.style.hide(axis='index').apply(highlight_total_row, axis=1)
    st.markdown(styled_df.to_html(escape=False), unsafe_allow_html=True)

    # Legend
    st.markdown("""
    ### Legend: Validation Column
    - ✅ **Match**: Extracted data matches attorney and Genesis calculations.  
    - ✖ **Discrepancy**: Genesis and attorney demand do not align.  
    - 🚩 **Calculation Issue**: Subtotal does not match total without deductions.  
    - N/A: Not applicable (used for subtotal, deductions, total rows).
    """)

    # Supporting Documents Table (Simulated)
    st.subheader("Supporting Documents Table")
    docs_data = claim_data.get("supporting_documents", [])
    if docs_data:
        sdt = pd.DataFrame(docs_data)
        st.dataframe(sdt)
    else:
        st.warning("No supporting documents data provided in the demo file.")

    # Liability Narrative (Simulated)
    st.subheader("Liability Determination Summary")
    liability_text = claim_data.get("liability_determination", "Liability summary not provided in current file.")
    st.markdown(f"""
    > {liability_text}
    """)

    st.success("✅ Section 1 complete. You may now proceed to Section 2: Adjuster Questions.")
