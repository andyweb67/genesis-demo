# 3_RRT_and_Zap.py

import streamlit as st
import pandas as pd

st.title("Section 3 – Reconciliation Review Table (RRT) & Zap Responses")

# Load required data
if 'claim_data' not in st.session_state or 'adjuster_summary' not in st.session_state:
    st.warning("Missing data from previous sections. Complete Sections 1 and 2 first.")
    st.stop()

claim = st.session_state.claim_data
adjuster = st.session_state.adjuster_summary

# Helper: Determine IME Shield
def is_shielded():
    return adjuster.get("ime_ordered", "No") == "No"

# RRT Data Construction
st.subheader("📊 Reconciliation Review Table (RRT)")
gds = claim['gds_table']
rrt_rows = []

# Basic row generator
def add_rrt_row(label, att_val, adj_val, ime):
    zap = ""
    if att_val != adj_val:
        if ime == "Shielded":
            zap = "🔒 Shielded – No IME, adjustment not allowed"
        else:
            zap = "⚠ Zap Counterstrike Triggered"
    return {
        "Damages": label,
        "Attorney Demand": f"${att_val}",
        "Adjuster Input": f"${adj_val}",
        "IME Status": ime,
        "Zap Response": zap
    }

# Medical Specials Total (roll up)
ms_att = gds['medical_specials_total']['attorney']
ms_adj = sum([
    float(p.get('adjuster_eval', 0).replace("$", "") or 0)
    for p in adjuster.get('medical_specials_eval', [])
])
rrt_rows.append(add_rrt_row("Medical Specials Total", ms_att, round(ms_adj, 2), "Shielded" if is_shielded() else "IME-Ordered"))

# Providers
for p in gds['providers']:
    prov_name = p['name']
    att_val = p['attorney']
    matching_input = next((item for item in adjuster.get('medical_specials_eval', []) if item['provider'] == prov_name), {})
    adj_val = matching_input.get('adjuster_eval', p['genesis'])
    ime_status = "Shielded" if is_shielded() else "IME-Ordered"
    rrt_rows.append(add_rrt_row(prov_name, att_val, adj_val, ime_status))

# P&S
att_ps = gds['pain_and_suffering']['attorney']
adj_ps = adjuster.get('pain_and_suffering', "0")
rrt_rows.append(add_rrt_row("Pain & Suffering", att_ps, adj_ps, "N/A"))

# Future Medicals, Lost Wages, Mileage
for label, key in [
    ("Future Medicals", "future_medicals"),
    ("Lost Wages", "lost_wages"),
    ("Mileage", "mileage")
]:
    att_val = gds[key]['attorney']
    adj_val = claim.get('adjuster_values', {}).get(key, gds[key].get('genesis', 0))
    rrt_rows.append(add_rrt_row(label, att_val, adj_val, "Shielded" if is_shielded() else "IME-Ordered"))

# Totals (auto-calculated)
sub_att = gds['subtotal']['attorney']
tot_att = gds['total']['attorney']
sub_adj = sum([
    float(r['Adjuster Input'].replace("$", "") or 0)
    for r in rrt_rows if r['Damages'] not in ["Deductions", "TOTAL"]
])

deduction = 0  # Placeholder
rrt_rows.append(add_rrt_row("Sub-Total", sub_att, round(sub_adj, 2), "N/A"))
rrt_rows.append(add_rrt_row("Deductions", 0, deduction, "N/A"))
rrt_rows.append(add_rrt_row("TOTAL", tot_att, round(sub_adj - deduction, 2), "N/A"))

# Display the RRT table
df_rrt = pd.DataFrame(rrt_rows)
st.dataframe(df_rrt)

# Pain & Suffering Comparison Table
st.subheader("📈 Pain & Suffering Comparison Table")
try:
    ps_mult_att = 4.482
    ps_calc_att = float(gds['pain_and_suffering']['attorney'])
    ms_calc = float(gds['medical_specials_total']['genesis'])
    ps_calc_adj = float(adjuster.get('pain_and_suffering', 0))
    ps_mult_adj = round(ps_calc_adj / ms_calc, 2) if ms_calc else 0

    ps_df = pd.DataFrame([
        {
            "Source": "Attorney Demand",
            "Medical Specials": f"${ms_calc}",
            "P&S Multiplier": f"{ps_mult_att}x",
            "Total P&S": f"${ps_calc_att}"
        },
        {
            "Source": "Adjuster Input",
            "Medical Specials": f"${ms_calc}",
            "P&S Multiplier": f"{ps_mult_adj}x",
            "Total P&S": f"${ps_calc_adj}"
        }
    ])
    st.dataframe(ps_df)
except Exception as e:
    st.warning(f"Could not generate comparison table: {e}")

st.success("✅ RRT and P&S comparison complete. Proceed to Section 4: Final Demand and Prophet.")
