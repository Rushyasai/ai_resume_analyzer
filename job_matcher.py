"""Modules 4-6: role dataset, TF-IDF + cosine similarity, skill-gap analysis.

Match score = 70% skill coverage (required skills found) + 30% TF-IDF cosine
similarity between the resume skill list and the role skill list.
These are estimates for guidance, not recruiter decisions.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA = Path(__file__).parent / "data"
W_COVERAGE, W_COSINE = 0.7, 0.3


def load_roles() -> pd.DataFrame:
    df = pd.read_csv(DATA / "job_roles.csv")
    df["skills"] = df["required_skills"].str.split(";")
    return df


def _tokens(text: str) -> list[str]:
    return [t.strip().lower() for t in text.split(";") if t.strip()]


def rank_roles(resume_skills: list[str]) -> pd.DataFrame:
    roles = load_roles()
    have = {s.lower() for s in resume_skills}
    docs = [";".join(s) for s in roles["skills"]] + [";".join(resume_skills)]
    vec = TfidfVectorizer(analyzer=_tokens)
    mat = vec.fit_transform(docs)
    cos = cosine_similarity(mat[-1], mat[:-1]).ravel() if resume_skills else np.zeros(len(roles))
    rows = []
    for i, r in roles.iterrows():
        req = r["skills"]
        cov = sum(s.lower() in have for s in req) / len(req)
        score = 100 * (W_COVERAGE * cov + W_COSINE * cos[i])
        rows.append({"Role": r["role"], "Match Score": round(score, 1),
                     "Coverage %": round(100 * cov, 1), "Cosine %": round(100 * cos[i], 1)})
    return pd.DataFrame(rows).sort_values("Match Score", ascending=False).reset_index(drop=True)


def skill_gap(resume_skills: list[str], role: str) -> tuple[list[str], list[str]]:
    roles = load_roles()
    required = roles.loc[roles["role"] == role, "skills"].iloc[0]
    have = {s.lower() for s in resume_skills}
    found = [s for s in required if s.lower() in have]
    missing = [s for s in required if s.lower() not in have]
    return found, missing
