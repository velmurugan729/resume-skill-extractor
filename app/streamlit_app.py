import streamlit as st
from pdf_parser import PDFParser
from llm_parser import LLMParser
from config import settings
import tempfile
import json
import time

# App metadata
st.set_page_config(
    page_title="Resume Extractor",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Resume Data Extractor")
st.markdown("Upload PDF resumes to extract structured data including name, email, phone, skills, experience, and education.")

# Sidebar controls
with st.sidebar:
    st.header("Settings")
    use_llm = st.checkbox("Use AI (LLM) for extraction", value=True)
    show_raw = st.checkbox("Show Raw JSON", value=False)

# Initialize parsers
pdf_parser = PDFParser()
llm_parser = LLMParser(settings.llm_api_key) if settings.llm_api_key else None

# Upload resumes
uploaded_files = st.file_uploader(
    "Upload Resume PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    progress_bar = st.progress(0)
    results = []

    for i, uploaded_file in enumerate(uploaded_files):
        try:
            with tempfile.NamedTemporaryFile(delete=True) as temp:
                temp.write(uploaded_file.read())
                temp.flush()

                text = pdf_parser.extract_text(temp.name)
                result = pdf_parser.extract_basic_info(text)

                if use_llm and llm_parser:
                    with st.spinner(f"Using LLM to extract {uploaded_file.name}..."):
                        llm_result = llm_parser.extract_data(text)
                        result.update(llm_result)

                results.append(result)
                progress_bar.progress((i + 1) / len(uploaded_files))

        except Exception as e:
            st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")

    if results:
        st.success(f"✅ Processed {len(results)} resume(s) successfully.")

        tab1, tab2 = st.tabs(["📊 Summary View", "🧾 Raw JSON"])

        with tab1:
            for idx, res in enumerate(results):
                with st.expander(f"Resume {idx+1}: {res.get('name', 'Unknown')}"):
                    cols = st.columns([1, 2])

                    with cols[0]:
                        st.image("https://via.placeholder.com/150", width=150)
                        st.markdown(f"**👤 Name:** {res.get('name', 'N/A')}")
                        st.markdown(f"**📧 Email:** {res.get('email', 'N/A')}")
                        st.markdown(f"**📱 Phone:** {res.get('phone', 'N/A')}")

                    with cols[1]:
                        st.subheader("🛠 Skills")
                        st.write(", ".join(res.get('skills', [])) or "N/A")

                        st.subheader("💼 Experience")
                        for exp in res.get("experience", []):
                            st.markdown(f"- {exp.get('title', '')} at {exp.get('company', '')}")
                            st.caption(exp.get("duration", ""))

                        st.subheader("🎓 Education")
                        for edu in res.get("education", []):
                            st.markdown(f"- {edu.get('degree', '')}, {edu.get('institution', '')} ({edu.get('year', '')})")

        with tab2:
            if show_raw:
                st.json(results)

        # Download button
        st.download_button(
            label="📥 Download All Results as JSON",
            data=json.dumps(results, indent=2),
            file_name="resume_data.json",
            mime="application/json"
        )
