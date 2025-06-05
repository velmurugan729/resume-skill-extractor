import streamlit as st
from utils.pdf_reader import extract_text_from_pdf
from models.skill_extractor import extract_skills

st.title("Resume Skill Extractor")

# ✅ Define this BEFORE using it
uploaded_file = st.file_uploader("Upload a PDF resume", type="pdf")

# ✅ Then use it here
if uploaded_file is not None:
    text = extract_text_from_pdf(uploaded_file)

    st.subheader("Extracted Text:")
    st.text(text)

    skills = extract_skills(text)

    st.subheader("Extracted Skills:")
    st.write(skills)
