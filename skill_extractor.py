"""Module 3: dictionary-based skill extraction, grouped by category."""
import re
from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent / "data"


def load_dictionary() -> pd.DataFrame:
    df = pd.read_csv(DATA / "skill_dictionary.csv", keep_default_na=False)
    df["aliases"] = df["aliases"].apply(lambda a: [x for x in a.split("|") if x])
    return df


def _pattern(term: str) -> re.Pattern:
    # custom boundaries so C++, C#, .NET and CI/CD match correctly
    return re.compile(r"(?<![a-z0-9+#])" + re.escape(term.lower()) + r"(?![a-z0-9+#])")


def extract_skills(clean_text: str) -> dict[str, str]:
    """Return {skill: category} for every dictionary skill found in the text."""
    found = {}
    for _, row in load_dictionary().iterrows():
        terms = [row["skill"]] + row["aliases"]
        if any(_pattern(t).search(clean_text) for t in terms):
            found[row["skill"]] = row["category"]
    return found


def group_by_category(skills: dict[str, str]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {}
    for skill, cat in skills.items():
        groups.setdefault(cat, []).append(skill)
    return {c: sorted(s) for c, s in sorted(groups.items())}
