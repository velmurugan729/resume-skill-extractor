import streamlit as st
from utils.pdf_reader import extract_text_from_pdf
from models.skill_extractor import extract_all

st.title("📄 Resume Skill Extractor")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

if uploaded_file is not None:
    with st.spinner("Processing..."):
        text = extract_text_from_pdf(uploaded_file)
        data = extract_all(text)

    st.subheader("📋 Extracted Data")
    st.json(data)
