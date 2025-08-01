import os
import pandas as pd
import fitz  # PyMuPDF
import docx
import mimetypes

def save_uploaded_files(uploaded_files, upload_dir="uploaded_files"):
    os.makedirs(upload_dir, exist_ok=True)
    saved_paths = []

    for file in uploaded_files:
        file_path = os.path.join(upload_dir, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        saved_paths.append(file_path)

    return saved_paths

def extract_text_from_pdf(filepath):
    """Safely extract text from a PDF file using PyMuPDF."""
    try:
        text = ""
        with fitz.open(filepath) as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        return f"⚠️ Could not read PDF: {str(e)}"

def extract_text_from_docx(filepath):
    """Extracts text from Word (.docx) file."""
    try:
        doc = docx.Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        return f"⚠️ Could not read DOCX: {str(e)}"

def extract_text_from_txt(filepath):
    """Reads plain text file."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        return f"⚠️ Could not read TXT: {str(e)}"

def extract_data_from_csv(filepath):
    """Reads CSV into pandas DataFrame."""
    return pd.read_csv(filepath)

def extract_data_from_excel(filepath):
    """Reads Excel into pandas DataFrame."""
    return pd.read_excel(filepath)

def process_file(filepath):
    """Detect file type and process accordingly."""
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".pdf":
        return "text", extract_text_from_pdf(filepath)

    elif ext == ".docx":
        return "text", extract_text_from_docx(filepath)

    elif ext == ".txt":
        return "text", extract_text_from_txt(filepath)

    elif ext == ".csv":
        return "dataframe", extract_data_from_csv(filepath)

    elif ext in [".xls", ".xlsx"]:
        return "dataframe", extract_data_from_excel(filepath)

    else:
        return "text", f"⚠️ Unsupported file type: {ext}"
