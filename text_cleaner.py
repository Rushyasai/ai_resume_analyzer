"""Module 2: text cleaning. Keeps technical symbols such as C++, C# and .NET."""
import re

EMAIL = re.compile(r"\S+@\S+\.\S+")
PHONE = re.compile(r"(\+?\d[\d\s\-()]{8,}\d)")


def remove_personal_info(text: str) -> str:
    """Strip emails and phone numbers so they never influence scoring."""
    return PHONE.sub(" ", EMAIL.sub(" ", text))


def clean_text(text: str) -> str:
    text = remove_personal_info(text).lower()
    text = re.sub(r"[^a-z0-9+#.\-/\s]", " ", text)  # keep + # . - /
    text = re.sub(r"\s+", " ", text)
    return text.strip()
