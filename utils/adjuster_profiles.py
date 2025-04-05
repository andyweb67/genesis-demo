# utils/adjuster_profiles.py

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