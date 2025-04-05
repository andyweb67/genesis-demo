import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()
import time

def call_with_backoff(url, headers, data, retries=4):
    for attempt in range(retries):
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 429:
            wait_time = 2 ** attempt
            print(f"[!] Rate limited. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            response.raise_for_status()
            return response
    raise Exception("Failed after multiple retries due to rate limiting.")

API_KEY = os.getenv("API_KEY")

def build_extraction_prompt(demand_text):
    """Builds the AI prompt to extract structured claim data."""
    return [
        {
            "role": "system",
            "content": (
                "You are a legal-medical data extractor. "
                "Your task is to extract structured data from plaintiff demand package text. "
                "Return the result in valid JSON format. Do not invent information. "
                "Only extract what is clearly stated."
            )
        },
        {
            "role": "user",
            "content": (
                f"Please extract the following from this demand package:\n"
                "- List of injuries\n"
                "- ICD-10 codes (if mentioned)\n"
                "- Treatment delays or gaps\n"
                "- Dollar amounts (medical bills, wage loss, total demand, etc.)\n"
                "- Causation statements (direct or disputed)\n\n"
                "Here is the text:\n\n"
                f"{demand_text}"
            )
        }
    ]

def extract_and_save_demand(input_path, output_path):
    """Extracts claim data using OpenAI (via requests) and saves as JSON."""
    try:
        # Read the raw demand text
        with open(input_path, 'r', encoding='utf-8') as f:
            demand_text = f.read()

        # Build prompt
        messages = build_extraction_prompt(demand_text)

        # Prepare OpenAI request
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": 0.0,
            "max_tokens": 1500
        }

        # Call OpenAI API
        response = call_with_backoff(url, headers, data)
        result = response.json()

        # Extract result content
        ai_output = result['choices'][0]['message']['content'].strip()
        extracted_data = json.loads(ai_output)

        # Save to output file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(extracted_data, f, indent=2)

        print(f"[✓] Extraction complete. Data saved to: {output_path}")

    except Exception as e:
        print(f"[!] Error during extraction: {e}")
