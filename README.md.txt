# 📑 AI Report Generator Bot

An intelligent, GPU-accelerated Streamlit app that analyzes and summarizes documents using sentiment analysis, classification, automatic charting, and optional GPT-powered summarization.

---

## 🚀 Features

- 📁 **Multi-file Upload** — Supports PDF, DOCX, TXT, XLS, XLSX
- 🧠 **Two Analysis Modes**:
  - **Lite**: Uses TextBlob (fast and lightweight)
  - **Advanced**: Uses HuggingFace Transformers with GPU (if available)
- 📊 **Auto Charts** — Plots numeric Excel data using Plotly
- 📋 **AI Analysis** — Sentiment detection & content classification
- 🧠 **ChatGPT Summarization** — Optional GPT-3.5-based summaries
- 💾 **Report Generator** — Auto-saves detailed reports
- ⚡ **GPU Acceleration** — Automatically uses CUDA if available

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-report-generator.git
cd ai-report-generator
```

2. Install dependencies

```bash
pip install -r requirements.txt
```


3. Run the app

```bash
streamlit run main.py
```


🧠 Enable GPT Summarization (Optional)
Open the file:

```bash
modules/gpt_handler.py
```

Replace this line:

```python
OPENAI_API_KEY = "REPLACE_ME_WITH_YOUR_API_KEY"
with your actual OpenAI key:
```

```python
OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxx"
```
Launch the app and toggle the ✅ "Use ChatGPT for smarter summarization" option.

❗ Note: GPT summarization won't work unless the API key is set.



📁 Project Structure
```graphql
.
├── main.py                     # Streamlit application entry point
├── README.md                   # This file
├── requirements.txt            # Dependencies
├── uploaded_files/             # Uploaded input files (auto-saved)
├── generated_reports/          # Output summary reports
└── modules/
    ├── file_handler.py         # Handles file parsing and type detection
    ├── data_analyzer.py        # Sentiment & classification logic
    ├── gpt_handler.py          # GPT summarization module (key here!)
    └── report_generator.py     # Generates final reports

```


⚡ GPU Acceleration

If your device supports CUDA, the app will automatically use GPU for model inference.

On start:

```bash
Device set to use cuda:0
```

To improve performance: avoid analyzing large files sequentially — batch inputs where possible.



✅ To-Do / Enhancements
 Export reports in PDF format

 Excel multi-sheet support

 File-type icons and improved UI

 Chat-style summarization

👤 Author
Built with ❤️ Aditya Vishwakarma

