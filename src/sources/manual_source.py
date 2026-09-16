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
                    "description": "Looking for a Junior Data Analyst proficient in Python, SQL, Excel, Power BI, and Pandas to clean and visualize datasets. MCA or B.Tech CS/IT preferred.",
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
                    "description": "We are hiring an entry-level GenAI Developer with skills in Python, FastAPI, LLMs, RAG, Vector Databases, ChromaDB, and LangChain. 0-1 years exp.",
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
                    "title": "Senior Data Scientist",
                    "company": "Global Analytics Corp",
                    "location": "Mumbai",
                    "description": "Requires 6+ years of experience in deep learning, PyTorch, Kubernetes, and big data architecture.",
                    "url": "https://globalanalytics.com/careers/sr-data-scientist",
                    "source": "Manual / Test Seed",
                    "posted_at": datetime.utcnow() - timedelta(hours=10),
                    "skills": ["Python", "PyTorch", "Kubernetes", "Deep Learning"],
                    "experience_min": 6,
                    "experience_max": 10,
                    "education_required": "Ph.D or Master's",
                    "remote_type": "On-site",
                    "salary_info": "Salary not specified"
                }
            ]
        else:
            self.seed_jobs = seed_jobs

    def fetch_jobs(self) -> List[Dict[str, Any]]:
        return self.seed_jobs
