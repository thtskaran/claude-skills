#!/usr/bin/env python3
"""
Academic Paper PDF Template
============================
Copy this to /home/claude/generate_paper.py, fill in content, and run.

Dependencies:
    pip install reportlab Pillow cairosvg --break-system-packages -q
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (
    BaseDocTemplate, Paragraph, Spacer, PageBreak, Image,
    Table, TableStyle, HRFlowable, NextPageTemplate,
    PageTemplate, Frame
)


# ════════════════════════════════════════════
#  CONFIG — Edit per paper
# ════════════════════════════════════════════
PAPER_TITLE     = "Your Paper Title Here"
SHORT_TITLE     = "Short Title"
AUTHOR_NAME     = "Author Name"
AUTHOR_AFFIL    = "Affiliation"
AUTHOR_EMAIL    = "email@example.com"
PAPER_DATE      = "February 2026"
PAPER_SUBJECT   = "Subject Area"
OUTPUT_PATH     = "/home/claude/paper.pdf"

# ════════════════════════════════════════════
#  LAYOUT
# ════════════════════════════════════════════
PAGE_W, PAGE_H = letter
MARGIN     = 1 * inch
CONTENT_W  = PAGE_W - 2 * MARGIN

# ════════════════════════════════════════════
#  COLORS
# ════════════════════════════════════════════
DARK           = HexColor("#1a1a2e")
GRAY_TEXT      = HexColor("#555555")
LIGHT_GRAY     = HexColor("#999999")
TABLE_HDR_BG   = HexColor("#e8eaf6")
RULE_CLR       = HexColor("#c5cae9")
ALT_ROW_BG     = HexColor("#fafafa")

# ════════════════════════════════════════════
#  STYLES
# ════════════════════════════════════════════
_ss = getSampleStyleSheet()

def _s(name, **kw):
    parent = kw.pop('parent', _ss['Normal'])
    if name not in _ss.byName:
        _ss.add(ParagraphStyle(name, parent=parent, **kw))

_s('PaperTitle',        parent=_ss['Title'], fontName='Times-Bold', fontSize=16,
   leading=20, alignment=TA_CENTER, spaceAfter=6, textColor=DARK)
_s('PrePrint',          fontName='Times-Italic', fontSize=8, leading=10,
   alignment=TA_CENTER, textColor=LIGHT_GRAY)
_s('AuthorName',        fontName='Times-Bold', fontSize=11, leading=14,
   alignment=TA_CENTER, spaceAfter=2, textColor=DARK)
_s('AuthorInfo',        fontName='Times-Roman', fontSize=9.5, leading=12,
   alignment=TA_CENTER, spaceAfter=2, textColor=GRAY_TEXT)
_s('AbsHead',           fontName='Times-Bold', fontSize=10, leading=13,
   alignment=TA_CENTER, spaceAfter=6, textColor=DARK)
_s('AbsBody',           fontName='Times-Italic', fontSize=9.5, leading=13,
   alignment=TA_JUSTIFY, leftIndent=24, rightIndent=24, spaceAfter=4)
_s('Keywords',          fontName='Times-Roman', fontSize=9, leading=12,
   alignment=TA_JUSTIFY, leftIndent=24, rightIndent=24, spaceAfter=12)
_s('SectH',             parent=_ss['Heading1'], fontName='Times-Bold', fontSize=13,
   leading=16, spaceBefore=18, spaceAfter=8, textColor=DARK, alignment=TA_LEFT)
_s('SubsectH',          parent=_ss['Heading2'], fontName='Times-Bold', fontSize=11,
   leading=14, spaceBefore=14, spaceAfter=6, textColor=DARK, alignment=TA_LEFT)
_s('SubsubH',           parent=_ss['Heading3'], fontName='Times-BoldItalic', fontSize=10.5,
   leading=13, spaceBefore=10, spaceAfter=4, textColor=DARK, alignment=TA_LEFT)
_s('Body',              fontName='Times-Roman', fontSize=10, leading=13.5,
   alignment=TA_JUSTIFY, spaceAfter=6)
_s('FigCap',            fontName='Times-Roman', fontSize=9, leading=12,
   alignment=TA_CENTER, spaceBefore=6, spaceAfter=12, textColor=HexColor("#333"))
_s('TblNote',           fontName='Times-Italic', fontSize=8.5, leading=11,
   alignment=TA_LEFT, spaceBefore=4, spaceAfter=10, textColor=GRAY_TEXT)
_s('Eq',                fontName='Times-Roman', fontSize=10, leading=14,
   alignment=TA_CENTER, spaceBefore=8, spaceAfter=8, textColor=DARK)
_s('Ref',               fontName='Times-Roman', fontSize=8.5, leading=11,
   alignment=TA_JUSTIFY, leftIndent=18, firstLineIndent=-18, spaceAfter=3)
_s('AppHead',           parent=_ss['Heading1'], fontName='Times-Bold', fontSize=12,
   leading=15, spaceBefore=16, spaceAfter=8, textColor=DARK, alignment=TA_LEFT)
_s('TblCell',           fontName='Times-Roman', fontSize=9, leading=12, alignment=TA_LEFT)
_s('TblCellB',          fontName='Times-Bold',  fontSize=9, leading=12, alignment=TA_LEFT)


# ════════════════════════════════════════════
#  HELPERS
# ════════════════════════════════════════════
def p(text, style='Body'):
    return Paragraph(text, _ss[style])

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=RULE_CLR,
                      spaceBefore=8, spaceAfter=8)

def make_table(headers, rows, col_widths=None, note=None):
    """Create a table with proper Paragraph-wrapped cells."""
    cs, ch = _ss['TblCell'], _ss['TblCellB']
    data = [[Paragraph(f'<b>{h}</b>', ch) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), cs) for c in row])
    if col_widths is None:
        col_widths = [CONTENT_W / len(headers)] * len(headers)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0), TABLE_HDR_BG),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
        ('GRID',          (0,0), (-1,-1), 0.4, RULE_CLR),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 6),
        ('RIGHTPADDING',  (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [white, ALT_ROW_BG]),
    ]))
    elems = [t]
    if note:
        elems.append(Paragraph(note, _ss['TblNote']))
    return elems

def add_figure(story, img_path, caption, max_w=4.5, max_h=7.0):
    """Add an image with caption. Maintains aspect ratio, caps dimensions."""
    from PIL import Image as PILImage
    w_px, h_px = PILImage.open(img_path).size
    aspect = h_px / w_px
    fw = max_w * inch
    fh = fw * aspect
    if fh > max_h * inch:
        fh = max_h * inch
        fw = fh / aspect
    story.append(Spacer(1, 6))
    story.append(Image(img_path, width=fw, height=fh, hAlign='CENTER'))
    story.append(Paragraph(caption, _ss['FigCap']))


# ════════════════════════════════════════════
#  PAGE CALLBACKS
# ════════════════════════════════════════════
def _pg_first(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 8)
    canvas.setFillColor(LIGHT_GRAY)
    canvas.drawCentredString(PAGE_W/2, 0.5*inch, str(canvas.getPageNumber()))
    canvas.restoreState()

def _pg_later(canvas, doc):
    canvas.saveState()
    pg = canvas.getPageNumber()
    canvas.setFont('Times-Roman', 8)
    canvas.setFillColor(LIGHT_GRAY)
    canvas.drawCentredString(PAGE_W/2, 0.5*inch, str(pg))
    canvas.setFont('Times-Italic', 7.5)
    canvas.drawString(MARGIN, PAGE_H - 0.6*inch, SHORT_TITLE)
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.6*inch,
                           f"Preprint \u2014 {PAPER_DATE}")
    canvas.setStrokeColor(RULE_CLR)
    canvas.setLineWidth(0.3)
    canvas.line(MARGIN, PAGE_H - 0.65*inch, PAGE_W - MARGIN, PAGE_H - 0.65*inch)
    canvas.restoreState()


# ════════════════════════════════════════════
#  BUILD — Edit this with your paper content
# ════════════════════════════════════════════
def build():
    doc = BaseDocTemplate(OUTPUT_PATH, pagesize=letter,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=0.85*inch, bottomMargin=0.75*inch,
        title=PAPER_TITLE, author=AUTHOR_NAME,
        subject=PAPER_SUBJECT)

    frame = Frame(doc.leftMargin, doc.bottomMargin,
                  CONTENT_W, PAGE_H - doc.topMargin - doc.bottomMargin, id='main')
    doc.addPageTemplates([
        PageTemplate(id='first', frames=[frame], onPage=_pg_first),
        PageTemplate(id='later', frames=[frame], onPage=_pg_later),
    ])

    story = []

    # ── Title Block ──────────────────────
    story.append(Spacer(1, 0.1*inch))
    story.append(p("Preprint \u2014 Not Yet Peer-Reviewed", 'PrePrint'))
    story.append(Spacer(1, 0.15*inch))
    story.append(p(PAPER_TITLE, 'PaperTitle'))
    story.append(Spacer(1, 0.15*inch))
    story.append(p(AUTHOR_NAME, 'AuthorName'))
    story.append(p(AUTHOR_AFFIL, 'AuthorInfo'))
    story.append(p(AUTHOR_EMAIL, 'AuthorInfo'))
    story.append(Spacer(1, 0.05*inch))
    story.append(p(PAPER_DATE, 'AuthorInfo'))
    story.append(Spacer(1, 0.2*inch))
    story.append(hr())

    # ── Abstract ─────────────────────────
    story.append(p("Abstract", 'AbsHead'))
    story.append(p("Your abstract here...", 'AbsBody'))
    story.append(Spacer(1, 4))
    story.append(p("<b>Keywords:</b> keyword1, keyword2, keyword3", 'Keywords'))
    story.append(hr())
    story.append(NextPageTemplate('later'))

    # ── 1. Introduction ──────────────────
    story.append(p("1. Introduction", 'SectH'))
    story.append(p("Your introduction text here..."))

    # ── 2. Section ───────────────────────
    story.append(p("2. Background", 'SectH'))
    story.append(p("2.1 Subsection Title", 'SubsectH'))
    story.append(p("Body text goes here..."))

    # ── Example Table ────────────────────
    for elem in make_table(
        headers=['Column A', 'Column B', 'Column C'],
        rows=[['Data 1', 'Data 2', 'Data 3'],
              ['Data 4', 'Data 5', 'Data 6']],
        col_widths=[2.2*inch, 2.5*inch, 1.8*inch],
        note="<b>Table 1.</b> Description of this table."
    ):
        story.append(elem)

    # ── Example Figure ───────────────────
    # add_figure(story, "/home/claude/figure.png",
    #            "<b>Figure 1.</b> Caption text here.")

    # ── References ───────────────────────
    story.append(hr())
    story.append(p("References", 'SectH'))
    story.append(p(
        "Author, A. (2025). Paper title. <i>Journal Name, 10</i>(2), 100\u2013115.",
        'Ref'))

    # ── Build ────────────────────────────
    doc.build(story)
    print(f"PDF generated: {OUTPUT_PATH}")


if __name__ == "__main__":
    build()
