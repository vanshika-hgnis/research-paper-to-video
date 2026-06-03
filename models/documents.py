# models/document.py
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Figure:
    index: int
    caption: str
    page: int
    image_bytes: Optional[bytes] = None


@dataclass
class Section:
    title: str
    body: str
    page_start: int
    role: Optional[str] = None  # filled in Stage 2
    salience: Optional[float] = None  # filled in Stage 2


@dataclass
class PaperDocument:
    title: str
    abstract: str
    sections: list[Section]
    figures: list[Figure]
    raw_text: str
