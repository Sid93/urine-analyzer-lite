#!/usr/bin/env python3
"""
Simple script to convert the Markdown report to HTML
User can then print to PDF from browser (Ctrl+P -> Save as PDF)
"""

import re

# Read the markdown file
with open('/home/sandbox/Urine_Dipstick_Analyzer_Manufacturing_Report.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Simple markdown to HTML conversion
html_content = content

# Convert headers
html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
html_content = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html_content, flags=re.MULTILINE)

# Convert bold
html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)

# Convert italic
html_content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html_content)

# Convert code blocks
html_content = re.sub(r'```(\w*)\n(.*?)```', r'<pre><code class="\1">\2</code></pre>', html_content, flags=re.DOTALL)

# Convert inline code
html_content = re.sub(r'`(.+?)`', r'<code>\1</code>', html_content)

# Convert links
html_content = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html_content)

# Convert line breaks
html_content = html_content.replace('\n\n', '</p><p>')

# Create full HTML document
html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Urine Dipstick Analyzer Manufacturing Report</title>
    <style>
        @page {{
            size: A4;
            margin: 2cm;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 210mm;
            margin: 0 auto;
            padding: 20px;
            background: white;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            page-break-before: always;
        }}
        h1:first-of-type {{
            page-break-before: avoid;
        }}
        h2 {{
            color: #34495e;
            border-bottom: 2px solid #95a5a6;
            padding-bottom: 8px;
            margin-top: 30px;
        }}
        h3 {{
            color: #555;
            margin-top: 20px;
        }}
        h4 {{
            color: #666;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            font-size: 0.9em;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }}
        th {{
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border-left: 4px solid #3498db;
        }}
        pre code {{
            background: none;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 20px;
            margin-left: 0;
            color: #555;
            font-style: italic;
        }}
        .page-break {{
            page-break-after: always;
        }}
        @media print {{
            body {{
                margin: 0;
                padding: 0;
            }}
            h1, h2 {{
                page-break-after: avoid;
            }}
            table {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
<p>{html_content}</p>
</body>
</html>
"""

# Write HTML file
with open('/home/sandbox/Urine_Dipstick_Analyzer_Manufacturing_Report.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("HTML file created successfully!")
print("To convert to PDF:")
print("1. Open Urine_Dipstick_Analyzer_Manufacturing_Report.html in a web browser")
print("2. Press Ctrl+P (or Cmd+P on Mac)")
print("3. Select 'Save as PDF' as the destination")
print("4. Click 'Save'")

