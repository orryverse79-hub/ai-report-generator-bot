import pandas as pd
import PyPDF2
import os
import torch
from transformers import pipeline
from textblob import TextBlob
from .file_handler import process_file


def analyze_excel(file_path):
    try:
        df = pd.read_excel(file_path)
        summary = {
            "filename": os.path.basename(file_path),
            "type": "excel",
            "sheet_names": pd.ExcelFile(file_path).sheet_names,
            "columns": df.columns.tolist(),
            "num_rows": len(df),
            "sample_data": df.head(3).to_dict(orient="records")
        }
        return summary
    except Exception as e:
        return {"error": str(e)}


def analyze_pdf(file_path):
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"

        summary = {
            "filename": os.path.basename(file_path),
            "type": "pdf",
            "num_pages": len(reader.pages),
            "text_preview": text[:500]  # First 500 chars
        }
        return summary
    except Exception as e:
        return {"error": str(e)}


def analyze_sentiment(text):
    """Returns sentiment polarity and classification."""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        sentiment = "Positive 😊"
    elif polarity < -0.1:
        sentiment = "Negative 😞"
    else:
        sentiment = "Neutral 😐"
    return sentiment, polarity


# ✅ Load classification pipeline with GPU support if available
device = 0 if torch.cuda.is_available() else -1
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=device)

def classify_text(text, candidate_labels=None):
    if not candidate_labels:
        candidate_labels = ["Finance", "Education", "Medical", "Legal", "News", "Technology"]

    result = classifier(text[:1000], candidate_labels)
    top_label = result["labels"][0]
    top_score = round(result["scores"][0], 2)
    return top_label, top_score


def analyze_file(filepath):
    try:
        file_type, content = process_file(filepath)

        if file_type == "text":  # PDF/DOCX/TXT case
            sentiment_label, sentiment_score = analyze_sentiment(content)
            classification_label, classification_score = classify_text(content)

            return {
                "type": "pdf",
                "filename": os.path.basename(filepath),
                "num_pages": content.count("\f") + 1,
                "text_preview": content[:500] + "..." if len(content) > 500 else content,
                "sentiment": sentiment_label,
                "sentiment_score": round(sentiment_score, 2),
                "classification": classification_label,
                "classification_score": classification_score
            }

        elif file_type == "dataframe":  # Excel or CSV case
            return {
                "type": "excel",
                "filename": os.path.basename(filepath),
                "sheet_names": getattr(content, "sheet_names", ["Sheet1"]),
                "columns": list(content.columns),
                "num_rows": len(content),
                "sample_data": content.head(5).astype(str).values.tolist(),
            }

    except Exception as e:
        return {"error": str(e), "filename": os.path.basename(filepath)}
