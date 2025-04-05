from flask import Flask, request, jsonify
import json
import hashlib
import os
from pathlib import Path
from dotenv import load_dotenv
import requests  # 👈 replacing openai

load_dotenv()

# Retrieve API key from .env
OPENAI_API_KEY = os.getenv("API_KEY")

# Function to call OpenAI manually using requests
def chat_with_openai(prompt):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 100
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()


# Set root path regardless of where the script is run
BASE_DIR = Path(__file__).resolve().parent

# Local imports
from utils.extract_and_save import extract_and_save_demand
from utils.zap_engine import load_zap_rules, batch_zap_responses
from utils.decision_point import decide_next_action
from utils.prophet_writer import generate_prophet_summary
from utils.json_loader import load_json

app = Flask(__name__)

# Load JSON configurations
SECTION_1_JSON = "Section1_GDS_190325.json"
SECTION_2_JSON = "Section_2_Adjuster_Questions_Updated_20240319.json"
SECTION_3_JSON = "Section_3_RRT_Updated_20240319.json"
SECTION_4_JSON = "Section_4_Final_Demand_and_PLN_Updated_20240319.json"
SECTION_5_JSON = "Section_5_5_adjuster.json"

if os.path.exists(SECTION_1_JSON):
    with open(SECTION_1_JSON, "r") as file:
        section1_gds_config = json.load(file)
else:
    section1_gds_config = {}

if os.path.exists(SECTION_2_JSON):
    with open(SECTION_2_JSON, "r") as file:
        section2_adjuster_config = json.load(file)
else:
    section2_adjuster_config = {}

if os.path.exists(SECTION_3_JSON):
    with open(SECTION_3_JSON, "r") as file:
        section3_rrt_config = json.load(file)
else:
    section3_rrt_config = {}

if os.path.exists(SECTION_4_JSON):
    with open(SECTION_4_JSON, "r") as file:
        section4_final_demand_config = json.load(file)
else:
    section4_final_demand_config = {}

if os.path.exists(SECTION_5_JSON):
    with open(SECTION_5_JSON, "r") as file:
        section5_negotiation_config = json.load(file)
else:
    section5_negotiation_config = {}

# Utility function: SHA-256 hash for data anchoring
def hash_data(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

# Section 2 Validation
def validate_adjuster_responses(claim_data):
    errors = []
    workflow_steps = section2_adjuster_config.get("workflow", {}).get("steps", [])
    for step in workflow_steps:
        step_title = step.get("title", "Unknown Step")
        input_required = step.get("details", {}).get("input_required", None)
        if input_required and step_title not in claim_data:
            errors.append(f"Missing required input for: {step_title}")
    return errors

# Section 3 Validation
def validate_rrt(claim_data):
    errors = []
    categories = section3_rrt_config.get("reconciliation_review_table_structure", {}).get("categories", [])
    for category in categories:
        category_name = category.get("name", category) if isinstance(category, dict) else category
        adjuster_value = claim_data.get(category_name)
        genesis_value = section3_rrt_config.get("genesis_calculations", {}).get(category_name)
        if adjuster_value is not None and genesis_value is not None and adjuster_value != genesis_value:
            errors.append(f"Discrepancy in {category_name}: Adjuster input {adjuster_value} vs. Genesis {genesis_value}")
    return errors

# Section 4 Validation
def validate_final_demand(claim_data):
    errors = []
    if section4_final_demand_config.get("authorization", {}).get("require_attorney_approval", False):
        if not claim_data.get("attorney_approval", False):
            errors.append("Attorney approval required before final demand submission.")
    if section4_final_demand_config.get("claim_iq_suppression", {}).get("enabled", False):
        threshold = section4_final_demand_config.get("pain_suffering_comparison", {}).get("comparison_table", {}).get("rows", [{}])[1].get("adjuster_value", {}).get("Multiplier Used", 0)
        if claim_data.get("p_and_s_multiplier", 0) < threshold:
            errors.append("Claim IQ suppression detected: Adjuster P&S valuation is below historical benchmark.")
    return errors

# Section 5 Validation
def validate_negotiation_script(claim_data):
    errors = []
    negotiation_steps = section5_negotiation_config.get("sections", [])
    for step in negotiation_steps:
        if "script" in step:
            for dialog in step["script"]:
                if "step" in dialog and dialog["step"] not in claim_data:
                    errors.append(f"Missing negotiation step: {dialog['step']}")
    return errors
# Health check endpoint
@app.route("/health")
def health_check():
    return jsonify({"status": "Genesis backend running"}), 200

@app.route("/test_openai", methods=["GET"])
def test_openai():
    try:
        result = chat_with_openai("Say hello from Genesis!")
        reply = result['choices'][0]['message']['content']
        return jsonify({"message": reply}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# Main route
@app.route("/process_claim", methods=["POST"])
def process_claim():
    """Process claim data and apply strict validation rules from JSON."""
    try:
        claim_data = request.json
        missing_fields = [field for field in section1_gds_config.get("required_fields", []) if field not in claim_data]
        if missing_fields:
            return jsonify({"error": "Missing required fields", "fields": missing_fields}), 400

        # Section 2 validation
        adjuster_errors = validate_adjuster_responses(claim_data)
        if adjuster_errors:
            return jsonify({"error": "Adjuster response validation failed", "details": adjuster_errors}), 400

        # Section 3 validation
        rrt_errors = validate_rrt(claim_data)
        if rrt_errors:
            return jsonify({"error": "Reconciliation Review Table validation failed", "details": rrt_errors}), 400

        # Section 4 validation
        final_demand_errors = validate_final_demand(claim_data)
        if final_demand_errors:
            return jsonify({"error": "Final Demand validation failed", "details": final_demand_errors}), 400

        # Section 5: negotiation script check
        negotiation_errors = validate_negotiation_script(claim_data)
        if negotiation_errors:
            return jsonify({"error": "Settlement negotiation validation failed", "details": negotiation_errors}), 400

        # Section 5: decision logic
        decision = decide_next_action(
            updated_offer=claim_data.get("adjuster_offer", 0),
            attorney_threshold=claim_data.get("attorney_minimum", 0),
            adjuster_flags=claim_data.get("adjuster_flags", []),
            auto_approve_enabled=True
        )
        claim_data["system_decision"] = decision

        if decision == "TRIGGER_PROPHET":
            from utils.prophet_writer import generate_prophet_summary
            from utils.json_loader import load_json

            adjuster_data = claim_data.get("adjuster_data", {})  # fallback if not present
            prophet_summary = generate_prophet_summary(claim_data, adjuster_data)
            claim_data["prophet_summary"] = prophet_summary

            # Attach final demand + PLN text from config
            claim_data["final_demand"] = section4_final_demand_config.get("final_demand", "Final demand text not configured.")
            claim_data["pre_litigation_notice"] = section4_final_demand_config.get("pln_text", "PLN text not configured.")

        # Anchor the final data hash
        claim_data["data_anchor"] = hash_data(claim_data)

        return jsonify({
            "message": "Claim processed successfully",
            "processed_data": claim_data
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# === Entry Point ===
if __name__ == "__main__":
    extract_and_save_demand("data/sample_demand.txt", "data/extracted_demand.json")

    # ZAP Test
    adjuster_inputs = [
        "This was a low-speed impact with minor pain.",
        "Treatment was delayed by several weeks.",
        "We believe symptoms were pre-existing."
    ]
    zap_rules = load_zap_rules()
    matched_zaps = batch_zap_responses(adjuster_inputs, zap_rules)
    for match in matched_zaps:
        print("Adjuster said:", match["adjuster_input"])
        print("ZAP replied:", match["zap_response"])
        print("-----")

    # RRT Builder Test
    from utils.rrt_builder import build_rrt
    build_rrt(
        demand_data_path="data/extracted_demand.json",
        adjuster_data_path="data/adjuster_response.json"
    )

    # Decision Point Test
    decision = decide_next_action(
        updated_offer=18500,
        attorney_threshold=22000,
        adjuster_flags=["IME contradiction", "low-ball reasoning"],
        auto_approve_enabled=True
    )
    print("Decision Point Output:", decision)

    app.run(debug=True)

