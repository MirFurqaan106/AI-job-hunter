from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime

class JobSource(ABC):
    @abstractmethod
    def fetch_jobs(self) -> List[Dict[str, Any]]:
        """
        Fetches raw job dictionaries from the source.
        Expected format per item:
        {
            "title": str,
            "company": str,
            "location": str,
            "description": str,
            "url": str,
            "source": str,
            "posted_at": datetime,
            "skills": List[str],
            "experience_min": int,
            "experience_max": int,
            "education_required": str,
            "remote_type": str,
            "salary_info": str
        }
        """
        pass
