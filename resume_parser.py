"""Module 1/2: validate and extract text from PDF / DOCX (in memory, nothing stored)."""
from io import BytesIO

from docx import Document
from pypdf import PdfReader

ALLOWED = {"pdf", "docx", "txt"}
MAX_MB = 5


def validate_file(name: str, size_bytes: int) -> str | None:
    """Return an error message, or None if the file is acceptable."""
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    if ext not in ALLOWED:
        return "Unsupported file type. Please upload a PDF or DOCX resume."
    if size_bytes > MAX_MB * 1024 * 1024:
        return f"File too large. Maximum size is {MAX_MB} MB."
    return None


def extract_text(name: str, data: bytes) -> str:
    ext = name.rsplit(".", 1)[-1].lower()
    if ext == "pdf":
        reader = PdfReader(BytesIO(data))
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    if ext == "docx":
        doc = Document(BytesIO(data))
        parts = [p.text for p in doc.paragraphs]
        for table in doc.tables:
            for row in table.rows:
                parts.extend(cell.text for cell in row.cells)
        return "\n".join(parts)
    return data.decode("utf-8", errors="ignore")
