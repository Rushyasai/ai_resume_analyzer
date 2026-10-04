# AI Resume Analyzer and Job Recommendation System

NLP-based Streamlit app that scores how well a resume matches job roles, lists missing skills and builds a learning roadmap.

## Features
Upload PDF/DOCX, text extraction and cleaning (keeps C++, C#, .NET), dictionary-based skill extraction (50 skills, grouped by category), TF-IDF + cosine similarity matching against 8 roles, top-3 role recommendation, skill-gap analysis, weekly roadmap, match-score chart, downloadable report.

## Workflow
Upload -> Extract text -> Clean -> Extract skills -> Load roles -> TF-IDF/cosine + coverage -> Rank roles -> Missing skills -> Roadmap

## Setup
```
python -m venv venv
venv\Scripts\activate        # Windows (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
streamlit run app.py
```

## Match score
`score = 70% x skill coverage + 30% x TF-IDF cosine similarity` (resume skills vs role skills).

## Testing
`python tests/run_tests.py` compares expected vs actual top role for the sample resumes and writes `reports/evaluation_sheet.csv`.

## Responsible AI
Guidance only, not for hiring decisions. Emails/phones are stripped; gender, age, religion, nationality, photo, marital status and disability are never scored. Resumes are processed in memory and not stored. Scores are estimates; missing keywords do not always mean missing ability.

## Limitations
Keyword matching misses unlisted skills and synonyms; scanned PDFs need OCR; role data is small and manually defined. Future work: spaCy, Sentence Transformers, FastAPI, Docker, JD upload.

## Deployment
Push to GitHub, then deploy on Streamlit Community Cloud (main file: `app.py`).
