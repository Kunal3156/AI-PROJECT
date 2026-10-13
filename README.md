# TalentMatch AI — NLP Resume Screening System

A Streamlit project that compares PDF/DOCX resumes against a job description using TF-IDF vectorization, cosine similarity, and transparent skill-overlap scoring.

## Run locally (Windows)
Open PowerShell in this folder and run:

    py -m venv .venv
    .\.venv\Scripts\Activate.ps1
    py -m pip install --upgrade pip
    py -m pip install -r requirements.txt
    py -m streamlit run app.py

If dependencies are already installed, run: py -m streamlit run app.py

## Deploy on Streamlit Community Cloud
1. Create a GitHub repository and upload app.py, resume_engine.py, requirements.txt, README.md, PROJECT_REPORT.md, and test_resume_engine.py.
2. Select app.py as the main file when deploying.
3. Test the public app with a job description and two sample PDF/DOCX resumes.
4. Do not use real or confidential resumes in a public demo; use fictional sample documents.

No API key is required. Resume matching runs within the Streamlit app process.

## Tests
    py -m unittest test_resume_engine -v

## Scoring
Overall relevance = 65% TF-IDF cosine similarity + 35% detected job-skill coverage. This is a heuristic relevance score, not a hiring probability.

## Responsible use
This project assists human review and does not make hiring decisions. Scanned PDFs may require OCR. Rankings may miss synonyms and context.
