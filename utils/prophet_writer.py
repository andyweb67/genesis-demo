import json
import openai  # assuming you're using OpenAI, replace if needed
from .json_loader import load_json

def load_prophet_prompt():
    return load_json("config/prophet_prompt.json")

def generate_prophet_summary(claim_data, adjuster_data, model="gpt-3.5-turbo"):
    """
    Generates a litigation summary (Prophet narrative) using AI.
    """

    prompt_template = load_prophet_prompt()
    base_prompt = prompt_template.get("base_prompt", "")
    
    # Optional: include severity, undervaluation, IME mismatch, etc.
    context = {
        "Claim Summary": claim_data,
        "Adjuster Response": adjuster_data
    }

    user_prompt = f"{base_prompt}\n\nDATA:\n{json.dumps(context, indent=2)}"

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a litigation strategy expert."},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )

    return response["choices"][0]["message"]["content"]
