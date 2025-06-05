import streamlit as st
import tempfile
import os
from utils.pdf_reader import extract_text_from_pdf
from models.skill_extractor import extract_resume_info

st.set_page_config(page_title="Resume Skill Extractor", layout="centered")

st.title("📄 Resume Skill Extractor")

uploaded_file = st.file_uploader("Upload a Resume (PDF)", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    try:
        with st.spinner("Extracting data..."):
            text = extract_text_from_pdf(temp_path)
            extracted_data = extract_resume_info(text)
        st.success("Extraction complete!")

        st.subheader("🔍 Extracted Resume Data:")
        st.json(extracted_data)
    finally:
        os.remove(temp_path)
