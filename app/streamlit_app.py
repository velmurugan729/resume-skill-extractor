import streamlit as st
from pdf_parser import PDFParser
from llm_parser import LLMParser
from config import settings
import tempfile
import json
import time

# App config
st.set_page_config(
    page_title="Resume Extractor",
    page_icon="📄",
    layout="wide"
)

# Initialize parsers
pdf_parser = PDFParser()
llm_parser = LLMParser(settings.llm_api_key) if settings.llm_api_key else None

# UI Components
st.title("📄 Resume Data Extractor")
st.markdown("Upload PDF resumes to extract structured data")

# Sidebar controls
with st.sidebar:
    st.header("Settings")
    use_llm = st.checkbox("Use AI Extraction", value=True, help="Enable for enhanced parsing using LLM")
    show_raw = st.checkbox("Show Raw Data", value=False)

# File uploader
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
                
                # Extract text
                text = pdf_parser.extract_text(temp.name)
                
                # Basic extraction
                result = pdf_parser.extract_basic_info(text)
                
                # Enhanced extraction
                if use_llm and llm_parser:
                    with st.spinner(f"Processing {uploaded_file.name} with AI..."):
                        result.update(llm_parser.extract_data(text))
                
                results.append(result)
                
                # Update progress
                progress = (i + 1) / len(uploaded_files)
                progress_bar.progress(progress)
                
        except Exception as e:
            st.error(f"Failed to process {uploaded_file.name}: {str(e)}")
    
    # Display results
    if results:
        st.success(f"Processed {len(results)} resumes successfully!")
        
        # Tabbed interface
        tab1, tab2 = st.tabs(["Summary View", "Detailed Data"])
        
        with tab1:
            for i, result in enumerate(results):
                with st.expander(f"Resume {i+1}: {result.get('name', 'Unknown')}"):
                    cols = st.columns([1,2])
                    
                    with cols[0]:
                        st.image("https://via.placeholder.com/150", width=150)
                        st.markdown(f"**Name:** {result.get('name', 'N/A')}")
                        st.markdown(f"**Email:** {result.get('email', 'N/A')}")
                        st.markdown(f"**Phone:** {result.get('phone', 'N/A')}")
                    
                    with cols[1]:
                        st.subheader("Skills")
                        st.write(", ".join(result.get('skills', [])))
                        
                        st.subheader("Experience")
                        for exp in result.get('experience', [])[:3]:  # Show first 3
                            st.markdown(f"**{exp.get('title', '')}** at {exp.get('company', '')}")
                            st.caption(exp.get('duration', ''))
        
        with tab2:
            st.json([r for r in results])
            
        # Download button
        st.download_button(
            label="Download Results as JSON",
            data=json.dumps(results, indent=2),
            file_name="resume_data.json",
            mime="application/json"
        )
