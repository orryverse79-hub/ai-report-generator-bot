def generate_report(analysis_results):
    report_lines = []

    for result in analysis_results:
        if "error" in result:
            report_lines.append(f"❌ Error processing file {result.get('filename', 'Unknown')}: {result['error']}\n")
            continue

        if result["type"] == "excel":
            report_lines.append(f"📊 Excel File: {result['filename']}")
            report_lines.append(f"- Sheets: {', '.join(result['sheet_names'])}")
            report_lines.append(f"- Columns: {', '.join(result['columns'])}")
            report_lines.append(f"- Total Rows: {result['num_rows']}")
            report_lines.append("- Sample Data:")
            for row in result['sample_data']:
                report_lines.append(f"  • {row}")
            report_lines.append("\n")

        elif result["type"] == "pdf":
            report_lines.append(f"📄 PDF/Text File: {result['filename']}")
            report_lines.append(f"- Pages: {result['num_pages']}")
            report_lines.append(f"- Sentiment: {result.get('sentiment', 'N/A')} (Score: {result.get('sentiment_score', 'N/A')})")
            report_lines.append(f"- Classification: {result.get('classification', 'N/A')} (Confidence: {result.get('classification_score', 'N/A')})")
            report_lines.append(f"- Text Preview:\n{result['text_preview']}")
            report_lines.append("\n")

    return "\n".join(report_lines)
