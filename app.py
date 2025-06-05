import streamlit as st
import os, json
from utils.pdf_reader import extract_text_from_pdf
from utils.helpers import extract_email, extract_phone, extract_name
from models.skill_extractor import extract_skills_with_llm

st.set_page_config(page_title="Resume Skill Extractor", layout="wide")

st.title("📄 Resume Skill Extractor")
uploaded_files = st.file_uploader("Upload Resumes (PDF only)", accept_multiple_files=True, type="pdf")

if uploaded_files:
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("extracted", exist_ok=True)

    for file in uploaded_files:
        path = os.path.join("uploads", file.name)
        with open(path, "wb") as f:
            f.write(file.read())

        if uploaded_file is not None:
            text = extract_text_from_pdf(uploaded_file)

        resume_data = {
            "name": extract_name(text),
            "email": extract_email(text),
            "phone": extract_phone(text),
            "skills": extract_skills_with_llm(text),
        }

        json_path = f"extracted/{file.name.replace('.pdf', '.json')}"
        with open(json_path, "w") as jf:
            json.dump(resume_data, jf, indent=4)

        st.subheader(f"Extracted from {file.name}")
        st.json(resume_data)
