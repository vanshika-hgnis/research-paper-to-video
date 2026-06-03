# stages/s1_parse.py
import fitz  # PyMuPDF
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBox, LTFigure
from models.document import PaperDocument, Section, Figure
import re


def parse_pdf(path: str) -> PaperDocument:
    doc = fitz.open(path)
    sections = _extract_sections(doc)
    figures = _extract_figures(doc)
    raw_text = "\n".join(s.body for s in sections)
    title = _guess_title(doc)
    abstract = _find_abstract(sections)

    return PaperDocument(
        title=title,
        abstract=abstract,
        sections=sections,
        figures=figures,
        raw_text=raw_text,
    )


def _extract_sections(doc) -> list[Section]:
    sections = []
    current_title = "preamble"
    current_body = []
    current_page = 0

    for page_num, page in enumerate(doc):
        blocks = page.get_text("blocks")  # (x0,y0,x1,y1,text,block_no,block_type)
        for block in blocks:
            text = block[4].strip()
            if not text:
                continue
            if _is_heading(text):
                if current_body:
                    sections.append(
                        Section(
                            title=current_title,
                            body=" ".join(current_body),
                            page_start=current_page,
                        )
                    )
                current_title = text
                current_body = []
                current_page = page_num
            else:
                current_body.append(text)

    if current_body:
        sections.append(
            Section(
                title=current_title,
                body=" ".join(current_body),
                page_start=current_page,
            )
        )
    return sections


def _extract_figures(doc) -> list[Figure]:
    figures = []
    idx = 0
    for page_num, page in enumerate(doc):
        # Find caption text near images
        blocks = page.get_text("blocks")
        for block in blocks:
            text = block[4].strip()
            if re.match(r"^(figure|fig\.?)\s*\d+", text, re.IGNORECASE):
                figures.append(Figure(index=idx, caption=text, page=page_num))
                idx += 1
    return figures


def _is_heading(text: str) -> bool:
    # Headings tend to be short, may start with a number, no trailing period
    return (
        len(text) < 80
        and not text.endswith(".")
        and (text[0].isupper() or re.match(r"^\d+\.?\s", text))
    )


def _guess_title(doc) -> str:
    # First large text block on page 0 is usually the title
    page = doc[0]
    blocks = sorted(
        page.get_text("dict")["blocks"],
        key=lambda b: (
            -b.get("lines", [{}])[0].get("spans", [{}])[0].get("size", 0)
            if b.get("lines")
            else 0
        ),
    )
    for block in blocks:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                if span.get("size", 0) > 14 and span.get("text", "").strip():
                    return span["text"].strip()
    return "Unknown Title"


def _find_abstract(sections: list[Section]) -> str:
    for s in sections:
        if "abstract" in s.title.lower():
            return s.body
    return sections[0].body if sections else ""
