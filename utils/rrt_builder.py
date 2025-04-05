import json
from utils.zap_engine import load_zap_rules, get_zap_response

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[!] Failed to load {path}: {e}")
        return {}

def build_rrt(demand_data_path, adjuster_data_path, zap_rules_path="config/zap_rules.json"):
    # Load data
    demand_data = load_json(demand_data_path)
    adjuster_data = load_json(adjuster_data_path)
    zap_rules = load_zap_rules(zap_rules_path)

    rrt_output = {
        "reconciliation_review_table": [],
        "pain_and_suffering_comparison": {}
    }

    # Define key categories to compare in RRT
    categories = [
        "Medical Bills",
        "Wage Loss",
        "Liability",
        "IME Status",
        "Pre-existing Conditions"
    ]

    for category in categories:
        adjuster_val = adjuster_data.get(category)
        genesis_val = demand_data.get(category)

        if adjuster_val is None or genesis_val is None:
            discrepancy = "Missing data"
        elif adjuster_val != genesis_val:
            discrepancy = f"{adjuster_val} ≠ {genesis_val}"
        else:
            discrepancy = "Match"

        zap_response = get_zap_response(str(adjuster_val), zap_rules)

        rrt_output["reconciliation_review_table"].append({
            "category": category,
            "adjuster_value": adjuster_val,
            "genesis_value": genesis_val,
            "discrepancy": discrepancy,
            "zap_response": zap_response if "No matching" not in zap_response else None
        })

    # Build P&S Comparison Sub-Table
    ps_adjuster = adjuster_data.get("P&S Multiplier")
    ps_attorney = demand_data.get("Attorney P&S Multiplier")
    ps_genesis = demand_data.get("Genesis Benchmark Multiplier")

    ps_discrepancy = None
    ps_zap_response = None

    if ps_adjuster and ps_genesis and ps_adjuster < ps_genesis:
        ps_discrepancy = f"{ps_adjuster} below benchmark"
        ps_zap_response = get_zap_response("p&s multiplier", zap_rules)

    rrt_output["pain_and_suffering_comparison"] = {
        "adjuster_multiplier": ps_adjuster,
        "attorney_multiplier": ps_attorney,
        "genesis_benchmark": ps_genesis,
        "discrepancy": ps_discrepancy,
        "zap_response": ps_zap_response
    }

    # Save output
    with open("data/rrt_output.json", "w", encoding="utf-8") as f:
        json.dump(rrt_output, f, indent=2)

    print("[✓] RRT and P&S Comparison Table built successfully.")
    return rrt_output
