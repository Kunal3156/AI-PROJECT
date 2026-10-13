# TalentMatch AI — NLP-Based Resume Screening System

## Abstract
TalentMatch AI compares multiple resumes with a job description. It extracts text from PDF and DOCX documents, transforms text with TF-IDF, calculates cosine similarity, detects a curated set of skills, and ranks resumes using an explainable relevance score.

## Problem Statement
Reviewing many resumes manually can be time-consuming. This project assists an initial review by identifying textual relevance between a job description and applicant documents. It is a decision-support tool, not an automated hiring decision-maker.

## Objectives
- Accept a job description and multiple resumes.
- Extract text from PDF and DOCX files.
- Identify job-related skills and qualification signals.
- Use TF-IDF vectorization and cosine similarity to compare documents.
- Combine text relevance and skill coverage into a transparent matching score.
- Rank candidates and export a CSV summary.

## Methodology
1. The user enters a job description and uploads candidate resumes.
2. PDF text is extracted using pypdf; DOCX text and tables are extracted using python-docx.
3. TF-IDF with unigram and bigram features transforms the job description and each resume into numerical vectors.
4. Cosine similarity measures relevance between the job-description vector and each resume vector.
5. A curated skill dictionary detects skills mentioned in the job description and resumes.
6. Skill coverage is calculated as matched job skills divided by detected job skills.
7. Overall relevance is 65% TF-IDF cosine similarity plus 35% detected job-skill coverage.
8. Candidates are ranked by combined score; matched and missing skills are shown for human review.

## Why this uses NLP
TF-IDF is a statistical text representation used in information retrieval and NLP. It weights terms based on their frequency within documents and rarity across the document collection. Cosine similarity compares the resulting vectors. This is a genuine NLP-based matching pipeline, but it is not a supervised classifier trained on labelled hiring outcomes. The score is not a probability of hiring success.

## Testing
Automated tests cover skill detection, ranking a clearly relevant resume above an unrelated resume, and empty input handling. Run:
py -m unittest test_resume_engine -v

## Limitations and Responsible Use
- Scanned image-only PDFs may need OCR, which is not included.
- The skill dictionary may miss synonyms, context, or skills not included.
- TF-IDF emphasizes word overlap and does not fully understand meaning.
- Education and experience extraction is a basic keyword signal and must be verified.
- The score is not calibrated and does not measure candidate quality or future job performance.
- Do not infer protected characteristics or automatically reject applicants. A human reviewer should assess complete applications consistently using job-related criteria.

## Conclusion
TalentMatch AI demonstrates document extraction, TF-IDF feature representation, cosine similarity, skill matching, ranking, testing, and an interactive interface. It is designed to reduce repetitive initial comparison while keeping hiring decisions with human reviewers.
