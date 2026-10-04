"""Evaluation sheet: python tests/run_tests.py"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from job_matcher import rank_roles
from skill_extractor import extract_skills
from text_cleaner import clean_text

cases = pd.read_csv(ROOT / "tests" / "test_cases.csv")
actual = []
for f in cases["test_resume"]:
    text = clean_text((ROOT / "sample_resumes" / f).read_text())
    actual.append(rank_roles(list(extract_skills(text))).iloc[0]["Role"])
cases["actual_top_role"] = actual
cases["result"] = (cases["expected_top_role"] == cases["actual_top_role"]).map({True: "PASS", False: "CHECK"})
print(cases.to_string(index=False))
cases.to_csv(ROOT / "reports" / "evaluation_sheet.csv", index=False)
