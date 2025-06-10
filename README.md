# Resume Skill Extractor

Resume Skill Extractor is an advanced tool designed to automatically extract structured information from resumes using a combination of state-of-the-art PDF parsers and powerful Natural Language Processing (NLP) and Large Language Models (LLMs). This tool helps recruiters, HR professionals, and job-matching platforms quickly parse and organize candidate data for efficient screening.

---

## 🚀 Features

- **Multi-field Extraction:**  
  Automatically extracts a wide range of information, including:
  - Name
  - Phone Number
  - Email Address
  - Total Experience
  - Education Details
  - Skills (hard & soft)
  - And more!

- **Multi-format Support:**  
  Parses resumes in common formats such as PDF, DOCX, and TXT.

- **Flexible PDF Extraction:**  
  Utilizes either **PyMuPDF** or **pdfminer** for robust and accurate PDF text extraction.

- **NLP & LLM Powered Parsing:**  
  - Uses advanced NLP models for classification of key fields, skills, and entities from resume text.
  - Leverages Large Language Models to intelligently parse and extract information from unstructured text.

- **Bulk Processing:**  
  Supports processing multiple resumes at once for large-scale recruitment needs.

- **Structured Output:**  
  Outputs extracted information in structured formats such as JSON or CSV for easy integration with other systems.

- **Customizable Dictionaries:**  
  Allows customization of skill and education dictionaries for domain-specific extraction.

- **JSON Output:**  
  Provides all extracted data in easy-to-use JSON format for seamless automation and integration.

---

## 🛠️ Usage

1. Place the resumes you want to process in the `input` directory.
2. Run the extraction script:
   ```bash
   python extract_resume_data.py --input ./input --output ./output
   ```
3. The extracted data will be available in the `output` directory in your chosen format (e.g., JSON, CSV).

---

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/velmurugan729/resume-skill-extractor.git
   cd resume-skill-extractor
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 📝 Configuration

- Edit the `skills_dictionary.json` or `education_dictionary.json` files to customize extraction rules.
- Adjust output format and processing options via command-line flags.

---

## 📦 Example Output (JSON)

```json
{
  "name": "Jane Smith",
  "email": "jane.smith@email.com",
  "phone": "+1-555-123-4567",
  "experience": "5 years",
  "education": [
    "B.Sc. Computer Science, XYZ University, 2018"
  ],
  "skills": [
    "Python", "Data Analysis", "Team Leadership"
  ]
}
```

---

## 🤝 Contributing

We welcome contributions! Feel free to open issues or submit pull requests for bug fixes, enhancements, or new features.

---

## 📜 License

This project is licensed under the MIT License.

---

*Created by [velmurugan729](https://github.com/velmurugan729)*
