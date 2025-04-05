import json

def load_zap_rules(filepath="config/zap_rules.json"):
    """
    Loads ZAP trigger-response rules from a JSON file.
    Each rule should include a 'trigger' and 'response'.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[!] Error loading ZAP rules: {e}")
        return []

def get_zap_response(adjuster_text, zap_rules):
    """
    Compares a single adjuster response to all ZAP triggers.
    Returns the first matching ZAP response.
    """
    adjuster_text = adjuster_text.lower()

    for rule in zap_rules:
        if rule["trigger"].lower() in adjuster_text:
            return rule["response"]
    
    return "No matching ZAP response found."

def batch_zap_responses(adjuster_inputs, zap_rules):
    """
    Processes a list of adjuster text inputs and returns all matching ZAP responses.
    Each result is a dictionary with the original input and matched response.
    """
    responses = []

    for input_text in adjuster_inputs:
        zap = get_zap_response(input_text, zap_rules)
        if zap and "No matching" not in zap:
            responses.append({
                "adjuster_input": input_text,
                "zap_response": zap
            })
    
    return responses
