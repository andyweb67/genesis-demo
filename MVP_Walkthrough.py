# Streamlit MVP Walkthrough for Genesis: "The Stakes Are Raised"

import streamlit as st

st.set_page_config(page_title="Genesis MVP: The Stakes Are Raised", layout="wide")

# Slide 1: The Disparity (Hook)
st.title("Genesis Claim Audit: The Stakes Are Raised")
st.header("Step 1: The Disparity")

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Attorney Demand", value="$72,500")
with col2:
    st.metric(label="Insurer Offer", value="$19,000", delta="-74%")

st.markdown("---")
st.subheader("Insurer software suppresses value. Attorneys hit a wall. But Genesis doesn't negotiate — it audits.")

# Slide 2: Post-Audit Movement
st.header("Step 2: Post-Audit Result")
col3, col4 = st.columns(2)
with col3:
    st.metric(label="Genesis Settlement Offer", value="$34,500", delta="+81.6%")
with col4:
    st.markdown("""
    **Before litigation. Before discovery.**
    
    Genesis triggered an increase without ever filing suit.
    """)

st.markdown("---")

# Slide 3: Why Did the Offer Increase?
st.header("Step 3: Why Did the Offer Increase?")
st.markdown("""
> Genesis doesn't plead for value. It forces recognition of it.

At every step, the insurer faces a choice:
- **Acknowledge value** and resolve fairly
- **Suppress value** and face escalating risk

Genesis exposes what traditional demand letters can't:
- Omitted severity inputs
- Claim IQ suppression patterns
- Adjuster script deviations
""")

# Slide 4: Chain Reaction (The Poker Table)
st.header("Step 4: The Chain Reaction")

st.markdown("""
Imagine the claim process as a poker game:

- **Lowball Bet** → $19,000 offer
- **Genesis Raises** → Audit exposes suppression
- **Insurer Calls or Folds** → Offer increases… or litigation begins

Here's how Genesis builds that pressure:

1. **Audit Module** – Genesis performs a forensic scan of the demand package, extracting dollar values, ICD-10 injury codes, and high-severity claims. It identifies what the insurer has omitted, downgraded, or ignored.

2. **Adjuster Interrogation** – A structured sequence of questions forces the adjuster to confirm or deny key facts: liability, IME status, software usage. Their responses are recorded and evaluated for consistency and fairness.

3. **ZAP Response Engine** – When an adjuster disputes a value without proper justification, Genesis instantly fires back a targeted rebuttal — grounded in medical facts, legal precedent, or jurisdictional data. These are called ZAPs.

4. **Reconciliation Review Table (RRT)** – This table compares the attorney's demand values with the insurer’s responses. Every conflict is highlighted. Every unjustified reduction becomes a documented point of exposure.

5. **Final Demand + Prophet Simulation** – If the insurer refuses to move, Genesis issues a final demand and runs a jury-facing simulation. This is where the insurer sees what happens when suppression is exposed in court.
""")

# Slide 5: What Happens If They Refuse?
st.header("Step 5: What Happens If They Refuse?")
st.markdown("""
If the insurer won’t move:
- Genesis pressures disclosure of Claim IQ ranges
- Extracts ALOG adjuster notes
- Compares historical settlement data
- Simulates jury impact using Prophet

> A jury doesn’t just see a claim — they see **suppression.**

That’s when the insurer realizes: they gambled… and lost.
""")

# Slide 6: How Genesis Works (Without Exposing the IP)
st.markdown("---")
st.header("How Genesis Works — Without Showing You the Engine")

st.markdown("""
Genesis is built for one thing: **results**.

It doesn’t require you to configure logic trees, weight multipliers, or navigate complex claim strategy.

It doesn’t teach you suppression tactics — it **neutralizes** them.

You don’t need to see the mechanics behind Genesis. In fact, you can’t.
That’s intentional.

> **The real leverage is protected in Genesis logic — not disclosed to the user.**

You see the outcome:
- Increased offer
- Documented suppression
- Escalation readiness

> *We don’t expose the engine. We expose the suppression.*
""")

# Final CTA
st.markdown("---")
st.header("Ready to See What’s Under the Hood?")
st.success("Genesis isn’t a demand generator. It’s what comes next.")

if st.button("👉 Let’s Open Genesis"):
    st.markdown("(Insert module walkthrough link or transition here)")
