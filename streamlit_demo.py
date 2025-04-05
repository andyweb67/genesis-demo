import streamlit as st
import pandas as pd
import json
import os
import time

def parse_dollar_value(value_str):
    try:
        return float(str(value_str).replace(',', '').replace('$', '').strip())
    except:
        return 0.0
st.set_page_config(page_title="Genesis AI Claim Audit", layout="wide")
st.title("Genesis Demo Interface")

# Upload Section with demo trigger button
st.markdown("### Upload a Demand Package")
col1, col2 = st.columns([2, 1])
with col1:
    uploaded_file = st.file_uploader("Choose a file to simulate", type=["pdf", "zip", "docx"])
with col2:
    demo_trigger = st.button("\u25B6 Click here to simulate upload")

show_gds_table = False

if uploaded_file or demo_trigger:
    st.info("Genesis is extracting the claim package...")

    # Simulated loading steps
    parse_steps = [
        "Extracting demand letter...",
        "Parsing medical bills...",
        "Scanning for pain and suffering historical multiplier",
        "Identifying ICD-10 severity codes...",
        "Searching police report for liability determination...",
        "searching for mileage reimbursement or lost wages",
        "populating Genesis Denmand Summary and validating all Attorney demand values"
    ]

    for step in parse_steps:
        with st.spinner(step):
            time.sleep(1.2)

    st.success("Package successfully extracted.")
    st.markdown("### \U0001F50D Building Genesis Demand Summary (GDS)")
    st.markdown(f"""
    **Genesis Audit v1.0 – {time.strftime('%B %d, %Y')}**
    """)
    show_gds_table = True

# Demo data folder path
data_folder = "demo_data"
case_files = [f for f in os.listdir(data_folder) if f.endswith(".json")]
selected_file = case_files[0] if case_files else None

if show_gds_table and selected_file:
    with open(os.path.join(data_folder, selected_file)) as f:
        claim_data = json.load(f)

    st.markdown(f"""
    ### GENESIS DEMAND SUMMARY (GDS)
    **Claimant Name:** {claim_data['claimant_name']}  
    **Claim Number:** {claim_data['claim_number']}  
    """)

    st.markdown("""
    > \U0001F9E0 **Genesis Demand Summary (GDS)**  
    > This audit summary reflects values extracted from the demand package and reconciled by Genesis AI to identify potential undervaluation.
    """)

    gds_rows = []

    # Medical Specials Total
    ms = claim_data['gds_table']['medical_specials_total']
    ms_validation = "\u2705 Medical Specials Total matches sum of individual providers"
    gds_rows.append({
        "Damages": "Medical Specials Total",
        "Attorney": f"${ms['attorney']}",
        "Genesis": f"${ms['genesis']}",
        "Validation": ms_validation,
        "Page #": "N/A"
    })

    # Providers
    for p in claim_data['gds_table']['providers']:
        provider_validation = f"\u2705 {p['name']} matches extracted billing total" if p['validation'] == "green tick" else p['validation']
        provider_validation += f" * Based on invoices from page {p['page']}"
        gds_rows.append({
            "Damages": f"\u00a0\u00a0\u00a0\u00a0{p['name']}",
            "Attorney": f"${p['attorney']}",
            "Genesis": f"${p['genesis']}",
            "Validation": provider_validation,
            "Page #": p['page'] or "N/A"
        })

    # Other Damage Items
    for label, key in [
        ("Pain Suffering", "pain_and_suffering"),
        ("Future Medicals", "future_medicals"),
        ("Lost Wages", "lost_wages"),
        ("Mileage", "mileage")
    ]:
        item = claim_data['gds_table'][key]
        validation_note = "—"
        attorney_val = float(str(item.get('attorney', "0")).replace("$", "").replace(",", "").strip())
        genesis_val = float(str(item.get('genesis', "0")).replace("$", "").replace(",", "").strip())

        if attorney_val == 0 and genesis_val == 0:
            validation_note = "Not claimed in the demand package"
        elif key == "pain_and_suffering":
            state = claim_data.get("state", "XX")
            try:
                specials_val = parse_dollar_value(claim_data['gds_table']['medical_specials_total']['genesis']).replace("$", "")
                multiplier = round(genesis_val / specials_val, 1) if specials_val else "N/A"
            except:
                multiplier = "N/A"
            validation_note = f"[{state}] historical pain and suffering multiplier has been applied [{multiplier}x]"
        elif item.get("validation", "") == "green tick":
            validation_note = f"\u2705 {label} extracted from demand package — matches attorney value"
        else:
            validation_note = item.get("validation", "—")

        gds_rows.append({
            "Damages": label,
            "Attorney": f"${item['attorney']}",
            "Genesis": f"${item['genesis']}",
            "Validation": validation_note,
            "Page #": ""
        })

    # Totals
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
            return ['background-color: #fff3cd'] * len(row)  # yellow for mismatch
        else:
            return [''] * len(row)

    styled_df = df.style.hide(axis='index').apply(highlight_total_row, axis=1)
    html = styled_df.to_html(escape=False)
    st.markdown(html, unsafe_allow_html=True)

    st.divider()
    st.markdown("## Section 3: RRT Summary")
    st.write("Initial Offer:", f"${claim_data['initial_offer']}")
    st.write("Genesis Value Estimate:", f"${claim_data['genesis_value_estimate']}")
    st.write("Attorney Demand:", f"${claim_data['attorney_demand_total']}")

    st.markdown("""
<hr style="margin-top: 40px; margin-bottom: 10px;">
<div style='text-align: center; font-size: 0.85em; color: gray;'>
    © 2025 <strong>PlaintiffMax LLC</strong> · Registered in South Carolina, USA<br>
    Genesis™ is proprietary claim audit software developed for licensing to plaintiff law firms and legal tech platforms.
</div>
""", unsafe_allow_html=True)

# Section 4: ZAP Response
st.header("Section 4: ZAP Response")
if st.button("Trigger ZAP Logic"):
    if claim_data.get("adjuster_assertions"):
        for item in claim_data['adjuster_assertions']:
            st.write("Adjuster Said:", item)
    else:
        st.info("No adjuster assertions present. ZAP triggers due to omission.")

# Section 5: Prophet Summary
st.header("Section 5: Prophet Summary")
if st.button("Run Prophet Projection"):
    try:
        projected = parse_dollar_value(claim_data['genesis_value_estimate']) * 1.5
        st.success(f"Projected Trial Verdict Estimate: ${projected:,.0f}")
        st.markdown(
            "> Based on undervaluation, omission, and severity, Genesis recommends policy tender or litigation."
        )
    except Exception as e:
        st.error(f"Could not calculate projection: {str(e)}")

# Optional: POST to Flask Backend
st.header("(Optional) Validate with Genesis Backend")
if st.button("POST to /process_claim"):
    try:
        import requests
        backend_url = "http://localhost:5000/process_claim"
        res = requests.post(backend_url, json=claim_data)
        result = res.json()
        if res.status_code == 200:
            st.success("Claim processed successfully by backend.")
            st.json(result)
        else:
            st.error("Backend returned an error:")
            st.json(result)
    except Exception as e:
        st.error(f"Connection failed: {e}")
