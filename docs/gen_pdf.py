#!/usr/bin/env python3
"""
Generate PDF docs for Urine Analyzer Lite:
  1. BOM (landscape table)
  2. README
  3. TODO checklist
  4. Merged combined doc

Run: python3 gen_pdf.py
Output: docs/  *.pdf + urine_analyzer_lite_docs.pdf
"""

import csv, re, os
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from pypdf import PdfWriter, PdfReader

# ── Paths ────────────────────────────────────────────────────────────────────
ROOT  = Path(__file__).parent.parent
DOCS  = ROOT / "docs"
BOM   = ROOT / "bom" / "bom.csv"
README= ROOT / "README.md"
TODO  = ROOT / "TODO.md"

DOCS.mkdir(exist_ok=True)

# ── Brand colours ─────────────────────────────────────────────────────────────
LEVRAM_BLUE  = colors.HexColor("#1B4F8A")
LEVRAM_LIGHT = colors.HexColor("#E8F0FA")
ROW_ALT      = colors.HexColor("#F5F7FA")
BORDER       = colors.HexColor("#AABCD0")
IMPORT_RED   = colors.HexColor("#C0392B")
NOTE_GRAY    = colors.HexColor("#6C7A89")

# ── Shared styles ─────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def style(name, **kw):
    s = ParagraphStyle(name, **kw)
    return s

TITLE  = style("DocTitle",  fontSize=22, leading=28, textColor=LEVRAM_BLUE,
               fontName="Helvetica-Bold", spaceAfter=4)
SUB    = style("DocSub",    fontSize=11, leading=14, textColor=NOTE_GRAY,
               fontName="Helvetica", spaceAfter=16)
H1     = style("H1",        fontSize=14, leading=18, textColor=LEVRAM_BLUE,
               fontName="Helvetica-Bold", spaceBefore=14, spaceAfter=6)
H2     = style("H2",        fontSize=11, leading=14, textColor=LEVRAM_BLUE,
               fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=4)
BODY   = style("Body",      fontSize=9,  leading=13, fontName="Helvetica",
               spaceAfter=4)
MONO   = style("Mono",      fontSize=8,  leading=11, fontName="Courier",
               spaceAfter=2, leftIndent=12)
SMALL  = style("Small",     fontSize=7.5, leading=10, fontName="Helvetica",
               textColor=NOTE_GRAY)
CELL   = style("Cell",      fontSize=7.5, leading=10, fontName="Helvetica",
               wordWrap="LTR")
CELL_B = style("CellBold",  fontSize=7.5, leading=10, fontName="Helvetica-Bold",
               wordWrap="LTR")
IMPORT_CELL = style("ImportCell", fontSize=7.5, leading=10, fontName="Helvetica",
                    textColor=IMPORT_RED, wordWrap="LTR")
NOTE_CELL   = style("NoteCell",   fontSize=6.5, leading=9,  fontName="Helvetica",
                    textColor=NOTE_GRAY, wordWrap="LTR")

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=8)

def header_para(text, subtitle=""):
    items = [Paragraph(text, TITLE)]
    if subtitle:
        items.append(Paragraph(subtitle, SUB))
    items.append(hr())
    return items

# ── Page header / footer callbacks ────────────────────────────────────────────
def make_page_fns(doc_title):
    def on_page(canvas, doc):
        canvas.saveState()
        # Header bar
        canvas.setFillColor(LEVRAM_BLUE)
        canvas.rect(doc.leftMargin, doc.height + doc.topMargin - 8*mm,
                    doc.width, 8*mm, fill=1, stroke=0)
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 9)
        canvas.drawString(doc.leftMargin + 4*mm,
                          doc.height + doc.topMargin - 5.5*mm, doc_title)
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(doc.leftMargin + doc.width - 4*mm,
                               doc.height + doc.topMargin - 5.5*mm,
                               "Levram Lifesciences — Confidential")
        # Footer
        canvas.setFillColor(NOTE_GRAY)
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(doc.leftMargin,
                          doc.bottomMargin - 6*mm,
                          "Urine Analyzer Lite  |  urine-analyzer-lite")
        canvas.drawRightString(doc.leftMargin + doc.width,
                               doc.bottomMargin - 6*mm,
                               f"Page {doc.page}")
        canvas.restoreState()
    return on_page, on_page

# ─────────────────────────────────────────────────────────────────────────────
# 1. BOM PDF
# ─────────────────────────────────────────────────────────────────────────────

def build_bom_pdf():
    out = DOCS / "bom.pdf"
    doc = SimpleDocTemplate(
        str(out), pagesize=landscape(A4),
        leftMargin=12*mm, rightMargin=12*mm,
        topMargin=20*mm, bottomMargin=14*mm,
    )
    on_page, on_first = make_page_fns("Bill of Materials — India Sourcing")
    story = []
    story += header_para(
        "Bill of Materials",
        "Urine Analyzer Lite  |  India Sourcing  |  Prices in INR (approx. ₹84 = $1 USD)"
    )

    # Read CSV
    with open(BOM, newline='', encoding='utf-8') as f:
        rows = list(csv.reader(f))

    # Columns to display (indices from original CSV):
    # 0=Ref 1=Name 2=Description 3=Cat 4=Type 5=Qty
    # 6=Unit INR 7=Total INR 8=India Supplier 9=India URL 10=Sourcing Note
    # We show: Ref, Name, Description, Qty, Unit ₹, Total ₹, Supplier, Note
    COL_IDX  = [0, 1, 2, 5, 6, 7, 8, 10]
    COL_HEAD = ["Ref", "Component", "Description", "Qty",
                "Unit\n(₹)", "Total\n(₹)", "India Supplier", "Sourcing Note"]
    # col widths in mm for landscape A4 (270mm usable)
    COL_W = [12, 38, 62, 9, 15, 15, 35, 64]

    col_w_pts = [w*mm for w in COL_W]

    header_row = [Paragraph(h, CELL_B) for h in COL_HEAD]
    table_data = [header_row]
    total_row_idx = None

    for r_idx, row in enumerate(rows[1:], start=1):  # skip CSV header
        if not any(row):
            continue
        ref = row[0].strip()
        # Detect TOTAL row
        is_total = ref == "" and any("TOTAL" in c for c in row)
        is_import = "IMPORT" in row[10] if len(row) > 10 else False

        cells = []
        for i, ci in enumerate(COL_IDX):
            val = row[ci].strip() if ci < len(row) else ""
            if is_total:
                p = Paragraph(val, CELL_B)
            elif is_import and i == 7:  # sourcing note col
                p = Paragraph(val, IMPORT_CELL)
            elif i == 7:  # note col
                p = Paragraph(val, NOTE_CELL)
            else:
                p = Paragraph(val, CELL)
            cells.append(p)
        table_data.append(cells)
        if is_total:
            total_row_idx = len(table_data) - 1

    tbl = Table(table_data, colWidths=col_w_pts, repeatRows=1)

    # Base style
    ts = TableStyle([
        # Header
        ("BACKGROUND",  (0,0), (-1,0), LEVRAM_BLUE),
        ("TEXTCOLOR",   (0,0), (-1,0), colors.white),
        ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0), (-1,0), 8),
        ("ALIGN",       (0,0), (-1,0), "CENTER"),
        ("VALIGN",      (0,0), (-1,-1), "TOP"),
        # Alternating rows
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, ROW_ALT]),
        # Grid
        ("GRID",        (0,0), (-1,-1), 0.3, BORDER),
        ("LINEBELOW",   (0,0), (-1,0), 1.0, LEVRAM_BLUE),
        # Padding
        ("TOPPADDING",  (0,0), (-1,-1), 2),
        ("BOTTOMPADDING",(0,0),(-1,-1), 2),
        ("LEFTPADDING", (0,0), (-1,-1), 3),
        ("RIGHTPADDING",(0,0), (-1,-1), 3),
        # Numeric cols right-align
        ("ALIGN",       (3,1), (5,-1), "RIGHT"),
    ])
    # Highlight total row
    if total_row_idx:
        ts.add("BACKGROUND",  (0, total_row_idx), (-1, total_row_idx), LEVRAM_LIGHT)
        ts.add("FONTNAME",    (0, total_row_idx), (-1, total_row_idx), "Helvetica-Bold")
        ts.add("LINEABOVE",   (0, total_row_idx), (-1, total_row_idx), 1.0, LEVRAM_BLUE)

    tbl.setStyle(ts)
    story.append(tbl)
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph(
        "<b>Note:</b> Items marked IMPORT require ordering via Mouser India (mouser.in) "
        "or element14 India (in.element14.com). Allow 1–2 week lead time. "
        "3D-printed parts use self-sourced PLA/PETG filament (~₹900–1200/kg on Amazon.in).",
        SMALL))

    doc.build(story, onFirstPage=on_first, onLaterPages=on_page)
    print(f"  Written: {out}")
    return out


# ─────────────────────────────────────────────────────────────────────────────
# 2. Markdown → PDF (shared renderer)
# ─────────────────────────────────────────────────────────────────────────────

def md_to_story(md_text, base_path=None):
    """Convert markdown to ReportLab flowables (no external lib needed)."""
    story = []
    lines = md_text.splitlines()
    in_code = False
    code_buf = []
    in_table = False
    table_buf = []

    def flush_code():
        nonlocal code_buf
        if not code_buf:
            return
        # Draw code block with background
        code_lines = "\n".join(code_buf)
        # Escape for ReportLab XML
        safe = code_lines.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
        paras = [Paragraph(l if l else " ", MONO) for l in safe.splitlines()]
        inner = Table([[p] for p in paras],
                      colWidths=[doc_width()],
                      style=[
                          ("BACKGROUND", (0,0),(-1,-1), colors.HexColor("#F0F3F6")),
                          ("LEFTPADDING",(0,0),(-1,-1), 6),
                          ("RIGHTPADDING",(0,0),(-1,-1),6),
                          ("TOPPADDING", (0,0),(-1,-1), 2),
                          ("BOTTOMPADDING",(0,0),(-1,-1),2),
                          ("BOX",(0,0),(-1,-1),0.5,BORDER),
                      ])
        story.append(Spacer(1,2*mm))
        story.append(inner)
        story.append(Spacer(1,2*mm))
        code_buf = []

    def flush_table():
        nonlocal table_buf
        if len(table_buf) < 2:
            table_buf = []
            return
        parsed = []
        for raw in table_buf:
            cells = [c.strip() for c in raw.strip("|").split("|")]
            parsed.append(cells)
        # row 1 = header, row 1 = separator (skip), rest = data
        header = parsed[0]
        data_rows = parsed[2:] if len(parsed) > 2 else []
        col_n = len(header)
        col_w = doc_width() / col_n

        def mcell(t, bold=False):
            s = CELL_B if bold else CELL
            safe = t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
            return Paragraph(safe, s)

        tdata = [[mcell(h, True) for h in header]]
        for row in data_rows:
            while len(row) < col_n:
                row.append("")
            tdata.append([mcell(c) for c in row[:col_n]])

        t = Table(tdata, colWidths=[col_w]*col_n, repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0,0),(-1,0), LEVRAM_BLUE),
            ("TEXTCOLOR",  (0,0),(-1,0), colors.white),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, ROW_ALT]),
            ("GRID",(0,0),(-1,-1),0.3,BORDER),
            ("VALIGN",(0,0),(-1,-1),"TOP"),
            ("TOPPADDING",(0,0),(-1,-1),2),
            ("BOTTOMPADDING",(0,0),(-1,-1),2),
            ("LEFTPADDING",(0,0),(-1,-1),4),
            ("RIGHTPADDING",(0,0),(-1,-1),4),
        ]))
        story.append(Spacer(1,2*mm))
        story.append(t)
        story.append(Spacer(1,2*mm))
        table_buf = []

    def inline(text):
        """Convert inline markdown (bold, code, tick boxes) to XML."""
        # Tick boxes
        text = text.replace("✅", "[DONE]").replace("🔲", "[ ]").replace("🔄", "[WIP]")
        # Escape XML chars first
        text = text.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
        # Bold **text**
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
        # Inline code `text`
        text = re.sub(r'`([^`]+)`', r'<font name="Courier" size="8">\1</font>', text)
        # Links [label](url) → label (url)
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        return text

    for line in lines:
        stripped = line.rstrip()

        # Code fence
        if stripped.startswith("```"):
            if in_code:
                flush_code()
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code_buf.append(stripped)
            continue

        # Table row
        if stripped.startswith("|"):
            in_table = True
            table_buf.append(stripped)
            continue
        elif in_table:
            flush_table()
            in_table = False

        # Headings
        if stripped.startswith("### "):
            story.append(Spacer(1,3*mm))
            story.append(Paragraph(inline(stripped[4:]), H2))
            continue
        if stripped.startswith("## "):
            story.append(Spacer(1,4*mm))
            story.append(Paragraph(inline(stripped[3:]), H1))
            story.append(HRFlowable(width="100%", thickness=0.3,
                                    color=BORDER, spaceAfter=4))
            continue
        if stripped.startswith("# "):
            continue  # title handled separately

        # Horizontal rule
        if stripped.startswith("---"):
            story.append(hr())
            continue

        # Bullet / checklist
        if stripped.startswith("- "):
            text = inline(stripped[2:])
            # Bold key items
            if "[DONE]" in text:
                text = text.replace("[DONE]", "<font color='#27AE60'>&#10003;</font>")
            elif "[ ]" in text:
                text = text.replace("[ ]", "<font color='#95A5A6'>&#9634;</font>")
            elif "[WIP]" in text:
                text = text.replace("[WIP]", "<font color='#E67E22'>&#8635;</font>")
            story.append(Paragraph(f"&nbsp;&nbsp;&bull;&nbsp;{text}", BODY))
            continue

        # Numbered list
        m = re.match(r'^(\d+)\.\s+(.*)', stripped)
        if m:
            story.append(Paragraph(f"&nbsp;&nbsp;<b>{m.group(1)}.</b>&nbsp;{inline(m.group(2))}", BODY))
            continue

        # Blockquote
        if stripped.startswith("> "):
            p = Paragraph(inline(stripped[2:]),
                          ParagraphStyle("BQ", parent=BODY,
                                         leftIndent=10, textColor=NOTE_GRAY,
                                         borderPad=4, borderColor=LEVRAM_BLUE,
                                         borderWidth=0))
            story.append(p)
            continue

        # Blank line
        if not stripped:
            story.append(Spacer(1, 2*mm))
            continue

        # Normal paragraph
        story.append(Paragraph(inline(stripped), BODY))

    if in_code:
        flush_code()
    if in_table:
        flush_table()

    return story

_doc_width = None
def doc_width():
    global _doc_width
    if _doc_width is None:
        _doc_width = A4[0] - 28*mm
    return _doc_width


def build_md_pdf(md_path, out_name, title, subtitle=""):
    out = DOCS / out_name
    doc = SimpleDocTemplate(
        str(out), pagesize=A4,
        leftMargin=14*mm, rightMargin=14*mm,
        topMargin=20*mm, bottomMargin=14*mm,
    )
    on_page, on_first = make_page_fns(title)
    story = header_para(title, subtitle)
    text = Path(md_path).read_text(encoding="utf-8")
    # Skip the H1 line (already in header)
    lines = text.splitlines()
    body = "\n".join(l for l in lines if not l.startswith("# ") or l.startswith("## "))
    story += md_to_story(body)
    doc.build(story, onFirstPage=on_first, onLaterPages=on_page)
    print(f"  Written: {out}")
    return out


# ─────────────────────────────────────────────────────────────────────────────
# 3. Merge all PDFs
# ─────────────────────────────────────────────────────────────────────────────

def merge_pdfs(pdf_paths, out_path):
    writer = PdfWriter()
    for p in pdf_paths:
        reader = PdfReader(str(p))
        for page in reader.pages:
            writer.add_page(page)
    with open(out_path, "wb") as f:
        writer.write(f)
    size_kb = Path(out_path).stat().st_size // 1024
    print(f"  Merged: {out_path}  ({size_kb} KB, {writer.get_num_pages()} pages)")


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Generating PDFs for Urine Analyzer Lite...")

    p1 = build_bom_pdf()

    p2 = build_md_pdf(
        README, "readme.pdf",
        title="Urine Analyzer Lite — Overview",
        subtitle="Setup, calibration, firmware, and operation guide"
    )

    p3 = build_md_pdf(
        TODO, "todo.pdf",
        title="Urine Analyzer Lite — Project Checklist",
        subtitle="Hardware · Firmware · Procurement · Integration · Regulatory"
    )

    combined = DOCS / "urine_analyzer_lite_docs.pdf"
    merge_pdfs([p1, p2, p3], combined)

    print("\nDone. Files in docs/:")
    for f in sorted(DOCS.glob("*.pdf")):
        print(f"  {f.name}  ({f.stat().st_size // 1024} KB)")
