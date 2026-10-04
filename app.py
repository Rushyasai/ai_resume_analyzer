"""Module 7: Streamlit dashboard. Run: streamlit run app.py"""
from datetime import datetime

import plotly.express as px
import streamlit as st

from job_matcher import load_roles, rank_roles, skill_gap
from resume_parser import extract_text, validate_file
from roadmap_generator import generate_roadmap
from skill_extractor import extract_skills, group_by_category
from text_cleaner import clean_text

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")
st.title("📄 AI Resume Analyzer & Job Recommendation System")
st.caption("Guidance tool for students. Scores are estimates, not recruiter decisions.")

roles = load_roles()["role"].tolist()
with st.sidebar:
    st.header("1. Upload")
    file = st.file_uploader("Resume (PDF or DOCX, max 5 MB)", type=["pdf", "docx", "txt"])
    st.header("2. Target role")
    target = st.selectbox("Choose a role", roles)
    st.info("Your resume is processed in memory and is not stored.")

if not file:
    st.write("👈 Upload a resume to begin.")
    st.stop()

error = validate_file(file.name, file.size)
if error:
    st.error(error)
    st.stop()
st.success(f"Uploaded: {file.name}")

try:
    raw = extract_text(file.name, file.getvalue())
except Exception as exc:  # corrupted or scanned file
    st.error(f"Could not read this file: {exc}")
    st.stop()

cleaned = clean_text(raw)
if len(cleaned) < 50:
    st.warning("Very little text was extracted (scanned PDF?). Try a text-based PDF or DOCX.")
    st.stop()

skills = extract_skills(cleaned)
ranking = rank_roles(list(skills))
found, missing = skill_gap(list(skills), target)
score = float(ranking.loc[ranking["Role"] == target, "Match Score"].iloc[0])

c1, c2, c3 = st.columns(3)
c1.metric(f"Match score: {target}", f"{score:.0f}%")
c2.metric("Skills detected", len(skills))
c3.metric("Required skills missing", len(missing))
if len(skills) < 20:
    st.caption("Tip: strong resumes usually list 20-30 relevant skills.")

st.subheader("Extracted skills")
for cat, items in group_by_category(skills).items():
    st.markdown(f"**{cat}:** " + ", ".join(items))

st.subheader("Match score by role")
fig = px.bar(ranking, x="Match Score", y="Role", orientation="h", range_x=[0, 100], text="Match Score")
fig.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig, use_container_width=True)

st.subheader("Top 3 recommended roles")
top3 = ranking.head(3)
for i, r in top3.iterrows():
    st.write(f"{i + 1}. **{r['Role']}** - {r['Match Score']:.0f}%")

st.subheader(f"Skill gap for {target}")
g1, g2 = st.columns(2)
g1.markdown("**Found in resume**")
g1.write(", ".join(found) or "None")
g2.markdown("**Missing or weak**")
g2.write(", ".join(missing) or "None - great coverage!")
st.caption("A missing keyword does not always mean missing ability; add it to your resume if you have it.")

st.subheader("Learning roadmap")
roadmap = generate_roadmap(missing)
for step in roadmap or ["No gaps found for this role."]:
    st.write("- " + step)

report = "\n".join([
    "AI RESUME ANALYSIS REPORT", f"Generated: {datetime.now():%Y-%m-%d %H:%M}",
    f"Target role: {target}", f"Match score: {score:.0f}%", "",
    "Skills found: " + ", ".join(found), "Missing skills: " + ", ".join(missing), "",
    "Recommended roles:", *[f"{i + 1}. {r['Role']} - {r['Match Score']:.0f}%" for i, r in top3.iterrows()], "",
    "Roadmap:", *roadmap, "",
    "Note: scores are estimates for guidance, not recruiter decisions.",
])
st.download_button("⬇️ Download analysis report", report, file_name="resume_analysis.txt")
