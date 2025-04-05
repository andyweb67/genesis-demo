import streamlit as st
import os
import json
from utils.extract_and_save import extract_and_save_demand

st.set_page_config(page_title="Genesis MVP", layout="wide")

st.title("🚀 Genesis Reboot: Claim Extraction Demo")

# File uploader
uploaded_file = st.file_uploader("Upload a demand .txt file", type=["txt"])

if uploaded_file:
    st.success("Demand file uploaded!")

    # Save the uploaded file temporarily
    input_path = "temp_input.txt"
    output_path = "temp_output.json"

    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())

    # Extract claim data
    with st.spinner("Extracting claim data using Genesis..."):
        extract_and_save_demand(input_path, output_path)

    # Display extracted results
    if os.path.exists(output_path):
        with open(output_path, "r") as f:
            extracted = json.load(f)
            st.subheader("📊 Extracted Claim Data")
            st.json(extracted)

        # Clean up
        os.remove(input_path)
        os.remove(output_path)
    else:
        st.error("Extraction failed. Check logs or backend.")
