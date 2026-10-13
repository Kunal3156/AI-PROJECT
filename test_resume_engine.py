import unittest
from resume_engine import analyze_resumes, detect_skills

class ResumeEngineTests(unittest.TestCase):
    def test_skill_detection(self):
        found=detect_skills("Python, SQL, pandas and machine learning.")
        for skill in ("python","sql","pandas","machine learning"):
            self.assertIn(skill,found)

    def test_relevant_resume_ranks_higher(self):
        jd="Junior Python Developer. Required skills: Python, SQL, pandas, machine learning. Build data analysis tools."
        candidates=[
            {"name":"Relevant.docx","text":"Python developer using Python, SQL, pandas and machine learning for data analysis projects."},
            {"name":"Unrelated.docx","text":"Experienced retail sales assistant. Customer service, inventory, merchandising and cash register."}
        ]
        results=analyze_resumes(jd,candidates)
        self.assertEqual(results[0]["name"],"Relevant.docx")
        self.assertGreater(results[0]["match_score"],results[1]["match_score"])
        self.assertIn("python",results[0]["matched_skills"])

    def test_empty_candidates(self):
        self.assertEqual(analyze_resumes("Python job",[]),[])

if __name__ == "__main__":
    unittest.main()
