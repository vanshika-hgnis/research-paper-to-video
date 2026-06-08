# main.py — wire it all together
from stages.s1_parse import parse_pdf
from stages.s2_analyze import analyze_paper


def run(pdf_path: str):
    print("Stage 1: parsing PDF...")
    doc = parse_pdf(pdf_path)
    print(f"  → {len(doc.sections)} sections, {len(doc.figures)} figures")

    print("Stage 2: semantic analysis...")
    doc = analyze_paper(doc)
    for s in doc.sections:
        print(f"  [{s.role:15s}] {s.salience:.2f}  {s.title[:50]}")

    return doc


if __name__ == "__main__":
    import sys

    run(sys.argv[1])
