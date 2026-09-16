from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel

class JobAnalysisResult(BaseModel):
    job_title: str
    company: str
    location: str
    experience_min: int = 0
    experience_max: int = 1
    education_required: str = "MCA / Computer Science / IT"
    remote_type: str = "On-site"
    salary_info: str = "Salary not specified"
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    summary: str = ""

class BaseAIProvider(ABC):
    @abstractmethod
    def analyze_job_description(self, raw_description: str) -> JobAnalysisResult:
        pass

class MockAIProvider(BaseAIProvider):
    def analyze_job_description(self, raw_description: str) -> JobAnalysisResult:
        # Fallback heuristic parser if Gemini API key is missing
        desc_lower = raw_description.lower()
        skills = []
        known_skills = ["Python", "SQL", "Excel", "Power BI", "Pandas", "NumPy", "FastAPI", "React", "Docker", "Machine Learning", "LLMs", "RAG"]
        for s in known_skills:
            if s.lower() in desc_lower:
                skills.append(s)
                
        return JobAnalysisResult(
            job_title="Discovered Job Role",
            company="Discovered Company",
            location="Bangalore",
            experience_min=0,
            experience_max=1,
            education_required="MCA / CS / IT",
            remote_type="Hybrid" if "hybrid" in desc_lower else ("Remote" if "remote" in desc_lower else "On-site"),
            salary_info="Salary not specified",
            required_skills=skills[:4],
            preferred_skills=skills[4:],
            summary="Extracted via heuristic mock parser."
        )
