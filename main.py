import streamlit as st
import os
from datetime import datetime
import plotly.express as px

from modules.file_handler import save_uploaded_files, process_file
from modules.report_generator import generate_report

# ✅ GPU/CPU Detection
try:
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    st.info(f"💻 Using device: **{device.upper()}**")
except ImportError:
    device = "cpu"
    st.warning("⚠️ PyTorch not installed. Defaulting to CPU.")

# 🔀 Mode selection
mode = st.radio("Choose Analysis Mode:", ["Lite", "Advanced"], horizontal=True)
use_advanced = mode == "Advanced"

# 🧠 GPT Toggle
use_gpt = st.checkbox("🧠 Use ChatGPT for smarter summarization", value=False)

# 🔁 Conditional import based on mode
if use_advanced:
    from modules.data_analyzer import analyze_sentiment, classify_text
else:
    def analyze_sentiment(text):
        from textblob import TextBlob
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            return "Positive 😊", polarity
        elif polarity < -0.1:
            return "Negative 😞", polarity
        else:
            return "Neutral 😐", polarity

    def classify_text(text):
        return "N/A", 0.0

# 🧠 GPT handler import
if use_gpt:
    from modules.gpt_handler import gpt_summary

# 🧠 App Config
st.set_page_config(page_title="📄 Report Generator Bot", layout="centered")
st.title("📑 AI Report Generator Bot")
st.write("Upload your PDF, Word, Text, or Excel files below, or enter custom text to generate automatic summaries and AI insights.")

# 📂 File uploader
uploaded_files = st.file_uploader(
    "Upload Files",
    type=["pdf", "docx", "txt", "xls", "xlsx"],
    accept_multiple_files=True,
    help="You can upload multiple files: PDF, DOCX, TXT, XLS, XLSX"
)
st.markdown("💡 *Supported file types: PDF, DOCX, TXT, XLS, XLSX*")

# 📝 Optional prompt input
st.markdown("### ✍️ Or enter custom text below:")
user_text = st.text_area("Custom Text Input", height=200, placeholder="Type or paste your own text for analysis...")

# 🔘 Analyze Button
if (uploaded_files or user_text.strip()) and st.button("🔍 Analyze Files/Text"):
    analysis_results = []

    # 🔍 Analyze user prompt
    if user_text.strip():
        with st.spinner("Analyzing custom text..."):
            if use_gpt:
                summary = gpt_summary(user_text)
                sentiment, sentiment_score = "N/A", 0.0
                category, category_score = "GPT Summary", 1.0
                text_preview = summary[:500]
            else:
                sentiment, sentiment_score = analyze_sentiment(user_text)
                category, category_score = classify_text(user_text)
                text_preview = user_text[:500]

            analysis_results.append({
                "filename": "User Prompt",
                "type": "pdf",
                "num_pages": 1,
                "text_preview": text_preview,
                "sentiment": sentiment,
                "sentiment_score": round(sentiment_score, 2),
                "classification": category,
                "classification_score": round(category_score, 2)
            })

    # 📁 Analyze uploaded files with per-file progress
    if uploaded_files:
        saved_paths = save_uploaded_files(uploaded_files)

        for i, path in enumerate(saved_paths):
            file_name = os.path.basename(path)
            st.markdown(f"### 📄 Processing: `{file_name}`")
            progress = st.progress(0, text="⏳ Starting...")

            try:
                file_type, content = process_file(path)
                progress.progress(30, text="📥 File loaded")

                if file_type == "text":
                    if use_gpt:
                        summary = gpt_summary(content)
                        sentiment, sentiment_score = "N/A", 0.0
                        category, category_score = "GPT Summary", 1.0
                        text_preview = summary[:1000]
                    else:
                        sentiment, sentiment_score = analyze_sentiment(content)
                        category, category_score = classify_text(content)
                        text_preview = content[:1000]

                    analysis_results.append({
                        "filename": file_name,
                        "type": "pdf",
                        "num_pages": content.count('\f') + 1,
                        "text_preview": text_preview,
                        "sentiment": sentiment,
                        "sentiment_score": round(sentiment_score, 2),
                        "classification": category,
                        "classification_score": round(category_score, 2)
                    })
                    progress.progress(100, text="✅ Completed")

                elif file_type == "dataframe":
                    df = content
                    sample_data = df.head(5).values.tolist()

                    st.subheader(f"📊 Auto-Generated Chart: {file_name}")
                    numeric_cols = df.select_dtypes(include='number').columns.tolist()

                    if len(numeric_cols) >= 2:
                        x_col, y_col = numeric_cols[0], numeric_cols[1]
                        fig = px.line(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info(f"No numeric columns available to plot in {file_name}")

                    analysis_results.append({
                        "filename": file_name,
                        "type": "excel",
                        "sheet_names": ["Sheet1"],
                        "columns": list(df.columns),
                        "num_rows": len(df),
                        "sample_data": sample_data
                    })
                    progress.progress(100, text="✅ Completed")

            except Exception as e:
                analysis_results.append({
                    "filename": file_name,
                    "error": str(e)
                })
                progress.progress(100, text="❌ Failed")

    # 💾 Save & show report
    report = generate_report(analysis_results)
    os.makedirs("generated_reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_filename = f"generated_reports/summary_report_{timestamp}.txt"

    with open(report_filename, "w", encoding="utf-8") as f:
        f.write(report)

    st.success(f"✅ Report auto-saved to: `{report_filename}`")
    st.subheader("📄 Generated Report")
    st.text_area("🧾 Report Content", report, height=400)

    if st.button("📥 Download Report as TXT"):
        st.download_button("Download TXT", data=report, file_name="summary_report.txt", mime="text/plain")

else:
    st.info("📤 Please upload at least one file or enter text to begin.")
