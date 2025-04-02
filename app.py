# MediVision AI - Advanced Medical Image Analysis 📊🩺

import streamlit as st
from pathlib import Path
import google.generativeai as genai
from api_key import api_key

# Configure API Key
genai.configure(api_key=api_key)

# Model Configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 8192,
}

# Safety Settings
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

# System Prompt for Medical Image Analysis
system_prompt = """
As a highly skilled medical practitioner specializing in image analysis, your task is to examine medical images for a renowned hospital. 
Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present.

Responsibilities:
1. **Detailed Analysis**: Examine the image carefully for abnormalities.
2. **Findings Report**: Document all observed anomalies or signs of disease.
3. **Recommendations and Next Steps**: Suggest potential further tests or treatments.
4. **Treatment Suggestions**: If applicable, provide possible treatment options.

**Important Notes**:
- Respond only if the image pertains to human health.
- If the image quality is poor, note that certain aspects may be 'Unable to be determined based on the provided image.'
- Always include the disclaimer: "Consult with a doctor before making any decisions."

Please provide the output in the following format:
- **Detailed Analysis**
- **Findings Report**
- **Recommendations and Next Steps**
- **Treatment Suggestions**

always bullets with numbers for each section.
"""

# Initialize Model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

# Streamlit UI Setup
st.set_page_config(page_title="Advanced Medical Image Analysis", page_icon=":robot:")
st.image("ai-doc-logo.png", width=100)
st.title("MediVision AI 📊🩺")
st.subheader("Advanced Medical Image Analysis")

# File Uploader
uploaded_file = st.file_uploader(
    "Upload the medical image for analysis", type=["jpg", "jpeg", "png"]
)
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Medical Image")

# Generate Report Button
if st.button("Generate Report"):
    if uploaded_file:
        image_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": "image/jpeg", "data": image_data}]
        prompt_parts = [image_parts[0], system_prompt]

        st.title("Analysis Report")
        st.write("Analyzing the image, please wait...")

        # Generate Analysis Report
        response = model.generate_content(prompt_parts)
        st.write(response.text)
    else:
        st.warning("Please upload an image before generating a report.")
