import streamlit as st
import pandas as pd
from resume_engine import analyze_resumes, extract_text

st.set_page_config(page_title="TalentMatch AI", page_icon="✦", layout="wide")
st.markdown("""<style>
:root{color-scheme:dark}.stApp,[data-testid="stAppViewContainer"]{background:#080d18;color:#e8edf8}
[data-testid="stHeader"]{background:#080d18}.block-container{max-width:1320px;padding-top:1.5rem;padding-bottom:3rem}
[data-testid="stSidebar"]{background:#0d1525;border-right:1px solid #25314a}[data-testid="stSidebar"] *{color:#dbe5f6}
.hero{padding:30px 34px;border:1px solid #2b3158;border-radius:22px;background:radial-gradient(circle at 88% 20%,#4c1d95 0,transparent 34%),linear-gradient(115deg,#10182a,#191d43 62%,#251653);margin-bottom:22px;box-shadow:0 15px 36px #0005}
.eyebrow{font-size:11px;font-weight:800;letter-spacing:2px;color:#c4b5fd}.hero h1{font-size:36px;color:#fff;margin:8px 0;font-weight:800;letter-spacing:-1px}.hero p{color:#c3cde3;margin:0;font-size:15px}
.section-title{font-size:22px;font-weight:800;color:#f4f6ff;margin-bottom:3px}.sub{font-size:13px;color:#9baaca;margin-bottom:16px}
[data-testid="stMetric"]{background:#111b2e;border:1px solid #293650;border-radius:15px;padding:16px}[data-testid="stMetricLabel"]{color:#9eacc7}[data-testid="stMetricValue"]{color:#f7f8ff}
[data-testid="stForm"]{background:#0e1728;border:1px solid #27344d;border-radius:18px;padding:22px}
[data-baseweb="select"]>div,[data-baseweb="input"]>div,[data-baseweb="textarea"]>div{background:#141f33!important;border-color:#34435e!important;color:#f5f7ff!important;border-radius:10px}
input,textarea,[data-baseweb="select"] *{color:#f5f7ff!important}
.stButton>button,.stDownloadButton>button{border-radius:11px;min-height:43px;font-weight:750;border:1px solid #7057db;background:linear-gradient(100deg,#713ee7,#4f46e5);color:white}
.stTabs [data-baseweb="tab-list"]{background:#10192a;border:1px solid #27334b;padding:5px;border-radius:12px;gap:6px}.stTabs [data-baseweb="tab"]{color:#aebbd2;border-radius:8px;padding:0 16px}.stTabs [aria-selected="true"]{background:#28204d;color:#c4b5fd}
[data-testid="stAlert"]{border-radius:12px}div[data-testid="stDataFrame"]{border:1px solid #27344d;border-radius:12px;overflow:hidden}.footer{color:#74829e;font-size:12px;text-align:center;padding:24px 0}
</style>""", unsafe_allow_html=True)
with st.sidebar:
    st.markdown("## ✦ TalentMatch AI")
    st.caption("NLP-POWERED RESUME ANALYSIS")
    st.divider()
    st.markdown("**How it works**")
    st.markdown("1. Paste a job description\n2. Upload PDF/DOCX resumes\n3. Compare relevance and skills\n4. Review ranked candidates")
    st.divider()
    st.markdown("**Methods used**")
    st.markdown("- TF-IDF text vectorization\n- Cosine similarity\n- Skill and qualification extraction")
    st.caption("Decision-support only · Human review required")
st.markdown('<div class="hero"><div class="eyebrow">NATURAL LANGUAGE PROCESSING · MACHINE LEARNING</div><h1>TalentMatch AI</h1><p>Compare resumes against a job description using text vectorization, relevance signals, and transparent skill matching.</p></div>',unsafe_allow_html=True)
m1,m2,m3=st.columns(3)
m1.metric("NLP METHOD","TF-IDF"); m2.metric("MATCH METHOD","Cosine similarity"); m3.metric("INPUT FORMATS","PDF · DOCX")
tab_analyze,tab_method,tab_about=st.tabs(["✦ Resume analysis","▥ How matching works","ⓘ About this project"])
with tab_analyze:
    st.markdown('<div class="section-title">Job requirements</div><div class="sub">Paste the full job description, including responsibilities, skills, and qualifications.</div>',unsafe_allow_html=True)
    jd=st.text_area("Job description",height=210,placeholder="We are hiring a Junior Python Developer...\nRequired skills: Python, SQL, pandas, scikit-learn...")
    uploads=st.file_uploader("Upload candidate resumes",type=["pdf","docx"],accept_multiple_files=True,help="Upload PDF or DOCX resumes. Scanned image-only PDFs may not contain extractable text.")
    analyze=st.button("Analyze and rank candidates →",type="primary",use_container_width=True)
    if analyze:
        if len(jd.strip())<40: st.error("Please enter a more complete job description (at least 40 characters).")
        elif not uploads: st.error("Upload at least one PDF or DOCX resume.")
        else:
            candidates=[]; errors=[]
            with st.spinner("Extracting resume text and calculating NLP similarity..."):
                for f in uploads:
                    try:
                        text=extract_text(f.getvalue(),f.name)
                        if len(text.strip())<30: errors.append(f"{f.name}: too little readable text. Scanned PDFs may need OCR.")
                        else: candidates.append({"name":f.name,"text":text})
                    except Exception as e: errors.append(f"{f.name}: {e}")
                if candidates:
                    st.session_state["analysis_results"]=analyze_resumes(jd,candidates)
                    st.session_state["analysis_jd"]=jd
            for err in errors: st.warning(err)
            if candidates: st.success(f"Analysis complete: {len(candidates)} resume(s) compared.")
    if "analysis_results" in st.session_state:
        results=st.session_state["analysis_results"]
        st.divider()
        st.markdown('<div class="section-title">Candidate ranking</div><div class="sub">Scores indicate textual relevance, not a guarantee of job performance.</div>',unsafe_allow_html=True)
        summary=[{"Rank":i,"Candidate":r["name"],"Overall match":f'{r["match_score"]:.1f}%',"TF-IDF relevance":f'{r["similarity"]:.1f}%',"Matched skills":len(r["matched_skills"]),"Missing listed skills":len(r["missing_skills"])} for i,r in enumerate(results,1)]
        st.dataframe(pd.DataFrame(summary),use_container_width=True,hide_index=True)
        st.download_button("↓ Download ranking (CSV)",pd.DataFrame(summary).to_csv(index=False),"talentmatch_ranking.csv","text/csv")
        for i,r in enumerate(results,1):
            with st.expander(f'{i}. {r["name"]} — {r["match_score"]:.1f}% match'):
                a,b=st.columns(2)
                with a:
                    st.metric("Overall match",f'{r["match_score"]:.1f}%'); st.progress(min(max(r["match_score"]/100,0),1))
                    st.caption(f'TF-IDF cosine similarity: {r["similarity"]:.1f}%')
                with b:
                    st.markdown("**Matched skills**"); st.write(", ".join(r["matched_skills"]) if r["matched_skills"] else "No supported skills detected.")
                    st.markdown("**Job skills not found**"); st.write(", ".join(r["missing_skills"]) if r["missing_skills"] else "No listed skills missing from detected matches.")
                st.markdown("**Education signals**"); st.write(", ".join(r["education"]) if r["education"] else "None detected")
                st.markdown("**Experience signals**"); st.write("; ".join(r["experience"]) if r["experience"] else "None detected")
        st.info("Use rankings to prioritize human review only. Missing keywords do not prove a candidate lacks a skill.")
with tab_method:
    st.markdown('<div class="section-title">Transparent NLP pipeline</div><div class="sub">Reproducible text processing rather than a black-box hiring decision.</div>',unsafe_allow_html=True)
    st.markdown("**1 · Text extraction**"); st.write("Reads selectable text from PDF and DOCX files.")
    st.markdown("**2 · TF-IDF vectorization**"); st.write("Transforms the job description and resumes into weighted term vectors.")
    st.markdown("**3 · Cosine similarity**"); st.write("Measures similarity between the job-description vector and each resume vector.")
    st.markdown("**4 · Skill overlap**"); st.write("Detects a curated set of skills and calculates the proportion of detected job skills found in each resume.")
    st.markdown("**5 · Combined score**"); st.write("Overall relevance = 65% TF-IDF cosine similarity + 35% job-skill coverage. This is a heuristic score, not a calibrated probability.")
    st.warning("TF-IDF + cosine similarity is an NLP information-retrieval method, not a supervised classifier trained on hiring outcomes.")
with tab_about:
    st.markdown('<div class="section-title">Project summary</div>',unsafe_allow_html=True)
    st.write("**Problem:** Reviewing many resumes manually can be time-consuming.")
    st.write("**Objective:** Extract resume text, identify job-related skill signals, and rank documents by relevance.")
    st.write("**Techniques:** TF-IDF, cosine similarity, skill extraction, PDF/DOCX parsing, transparent scoring.")
    st.write("**Limitations:** Scanned text, synonyms, and context may be missed; the skill dictionary is curated; similarity is not proof of candidate suitability.")
    st.write("**Responsible use:** A human reviewer must assess complete applications consistently using job-related criteria.")
st.markdown('<div class="footer">TALENTMATCH AI · PYTHON + SCIKIT-LEARN · NLP PROJECT</div>',unsafe_allow_html=True)
