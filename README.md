# 📄 AI Report Generator Bot

An intelligent Streamlit-based tool to auto-analyze and summarize uploaded documents like PDFs, Word files, Excel sheets, and plain text using classical and AI-powered techniques. Optionally integrates *ChatGPT (GPT-3.5 Turbo)* for smarter document summarization via a toggle switch.

---

## 🚀 Features

- 📥 Upload support for: .pdf, .docx, .txt, .xls, .xlsx
- 📊 Auto-charting for numerical Excel data
- 🔍 Sentiment and topic classification (Lite or Advanced)
- 🧠 Optional ChatGPT integration via a toggle (requires your OpenAI API key)
- 📁 Auto-saves report in generated_reports/
- 📝 Clean and simple UI built with Streamlit
- ⚙ Device-aware GPU/CPU setup (uses GPU if available)
- ✅ Apache 2.0 licensed for open contribution

---

## 🧠 GPT Integration (Optional)

Enable the "Use ChatGPT" checkbox in the app to use GPT-3.5 for summarization. To activate this:

1. Open the file: 
```
modules/gpt_handler.py
```

2. Replace the following line:

```python
OPENAI_API_KEY = "REPLACE_ME_WITH_YOUR_API_KEY"
```

with your actual OpenAI API key:

```
OPENAI_API_KEY = "sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

⚠ GPT functionality will remain disabled unless you add your key.


---

🖥 How to Run

1. Clone the repository:


```
git clone https://github.com/yourusername/ai-report-generator-bot.git
cd ai-report-generator-bot
```

2. Install dependencies:


```
pip install -r requirements.txt
```


3. (Required for sentiment analysis in Lite Mode)

```
python -m textblob.download_corpora
```


4. Launch the app:


```
streamlit run main.py
```



---

### Why it's needed:

- Without this step, **TextBlob sentiment analysis will fail silently** or throw `LookupError` related to missing corpora.
- It's not needed if GPT-only mode is used, but most users will try Lite mode first, so it's important.









---

📁 Project Structure
```
├── main.py
├── requirements.txt
├── README.md
├── LICENSE
├── generated_reports/
├── uploaded_files/
└── modules/
    ├── file_handler.py
    ├── data_analyzer.py
    ├── gpt_handler.py
    ├── report_generator.py
```



---

📜 License

This project is licensed under the Apache License 2.0 © 2025 Aditya Vishwakarma.




---

👨‍💻 Author

Aditya Vishwakarma


---

💡 Tips

📌 For best performance, install CUDA-compatible PyTorch if running on a GPU.


💬 Feedback and contributions are welcome!
