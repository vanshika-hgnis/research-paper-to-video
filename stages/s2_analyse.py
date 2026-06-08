# stages/s2_analyze.py — NIM client setup + first LLM call
from openai import OpenAI
from models.document import PaperDocument, Section
from config import NIM_API_KEY, NIM_BASE_URL, LLM_MODEL
import json

client = OpenAI(api_key=NIM_API_KEY, base_url=NIM_BASE_URL)

SECTION_ROLES = [
    "introduction",
    "related_work",
    "method",
    "results",
    "conclusion",
    "background",
    "other",
]


def analyze_paper(doc: PaperDocument) -> PaperDocument:
    doc.sections = [_classify_section(s) for s in doc.sections]
    return doc


def _classify_section(section: Section) -> Section:
    prompt = f"""You are analyzing a scientific paper section.
Classify this section and score its importance for an explanatory video.

Section title: {section.title}
Section body (first 400 chars): {section.body[:400]}

Respond with JSON only, no other text:
{{
  "role": one of {SECTION_ROLES},
  "salience": float 0.0-1.0 (1.0 = core contribution, 0.0 = boilerplate),
  "reason": one sentence
}}"""

    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=200,
    )
    raw = resp.choices[0].message.content.strip()
    try:
        data = json.loads(raw)
        section.role = data.get("role", "other")
        section.salience = float(data.get("salience", 0.5))
    except json.JSONDecodeError:
        section.role = "other"
        section.salience = 0.5
    return section
