from typing import List, Dict, Any
from datetime import datetime, timedelta
from src.sources.base import JobSource

class ManualJobSource(JobSource):
    def __init__(self, seed_jobs: List[Dict[str, Any]] = None):
        if seed_jobs is None:
            self.seed_jobs = [
                {
                    "title": "Junior Data Analyst",
                    "company": "Example Technologies",
                    "location": "Bangalore",
                    "description": "Looking for a Junior Data Analyst proficient in Python, SQL, Excel, Power BI, and Pandas.",
                    "url": "https://example.com/careers/jr-data-analyst-101",
                    "source": "Manual / Test Seed",
                    "posted_at": datetime.utcnow() - timedelta(hours=2),
                    "skills": ["Python", "SQL", "Excel", "Power BI", "Pandas"],
                    "experience_min": 0,
                    "experience_max": 1,
                    "education_required": "MCA / Computer Science / IT",
                    "remote_type": "Hybrid",
                    "salary_info": "₹4.5 - 6.5 LPA"
                },
                {
                    "title": "GenAI Developer",
                    "company": "AI Innovations Lab",
                    "location": "Bangalore (Remote Available)",
                    "description": "We are hiring an entry-level GenAI Developer with skills in Python, FastAPI, LLMs, RAG, Vector Databases, ChromaDB.",
                    "url": "https://aiinnovations.com/jobs/genai-dev-202",
                    "source": "Manual / Test Seed",
                    "posted_at": datetime.utcnow() - timedelta(hours=5),
                    "skills": ["Python", "FastAPI", "LLMs", "RAG", "ChromaDB", "Vector Databases", "Git"],
                    "experience_min": 0,
                    "experience_max": 1,
                    "education_required": "MCA / B.Tech CS",
                    "remote_type": "Remote",
                    "salary_info": "₹6.0 - 9.0 LPA"
                },
                {
                    "title": "Data Analyst — Freshers",
                    "company": "TechCorp India",
                    "location": "Bangalore",
                    "description": "Urgent hiring for Data Analyst freshers with skills in Python, SQL, Excel, Power BI, Pandas, Seaborn. MCA / CS graduates welcome!",
                    "url": f"https://techcorp-india.com/careers/data-analyst-{int(datetime.utcnow().timestamp())}",
                    "source": "Live Discovery",
                    "posted_at": datetime.utcnow() - timedelta(minutes=10),
                    "skills": ["Python", "SQL", "Excel", "Power BI", "Pandas", "Seaborn"],
                    "experience_min": 0,
                    "experience_max": 1,
                    "education_required": "MCA / CS / IT",
                    "remote_type": "Hybrid",
                    "salary_info": "₹5.0 - 7.0 LPA"
                }
            ]
        else:
            self.seed_jobs = seed_jobs

    def fetch_jobs(self) -> List[Dict[str, Any]]:
        return self.seed_jobs
