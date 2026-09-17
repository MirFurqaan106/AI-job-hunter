import requests
import xml.etree.ElementTree as ET
import urllib.parse
import re
import logging
from datetime import datetime
from typing import List, Dict, Any
from src.sources.base import JobSource

logger = logging.getLogger(__name__)

class LinkedInPublicJobSource(JobSource):
    """
    Ingests public LinkedIn job postings directly for India / Remote target roles.
    Fetches real LinkedIn job links (https://www.linkedin.com/jobs/view/...)
    """
    def __init__(self):
        self.target_searches = [
            ("Data Analyst", "Bangalore"),
            ("GenAI Developer", "India"),
            ("Python Developer", "Bangalore"),
            ("Business Analyst", "Bangalore"),
            ("Software Engineer", "Bangalore"),
            ("AI Engineer", "Remote")
        ]

    def fetch_jobs(self) -> List[Dict[str, Any]]:
        jobs = []
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }

        for role, location in self.target_searches:
            try:
                # Query public LinkedIn jobs RSS/Search feed
                query = urllib.parse.quote(f'site:linkedin.com/jobs/view "{role}" "{location}"')
                url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"

                res = requests.get(url, headers=headers, timeout=10)
                if res.status_code == 200:
                    root = ET.fromstring(res.text)
                    channel = root.find("channel")
                    if channel is not None:
                        for item in channel.findall("item")[:4]:
                            raw_title = item.findtext("title") or "LinkedIn Job"
                            raw_link = item.findtext("link") or ""
                            desc = item.findtext("description") or ""

                            # Extract company & title
                            title = raw_title
                            company = "Company on LinkedIn"
                            if " - " in raw_title:
                                parts = raw_title.split(" - ")
                                title = parts[0].strip()
                                company = parts[1].strip()

                            # Try to extract direct LinkedIn job URL from description or link
                            linkedin_match = re.search(r'https?://[a-zA-Z0-9\.\-]*linkedin\.com/jobs/view/[0-9]+', desc + " " + raw_link)
                            final_url = linkedin_match.group(0) if linkedin_match else raw_link

                            jobs.append({
                                "title": title,
                                "company": company,
                                "location": f"{location}, India",
                                "description": f"LinkedIn Job Posting for {title} at {company}. {desc}",
                                "url": final_url,
                                "source": "LinkedIn Public Source",
                                "posted_at": datetime.utcnow(), # Treated as current discovery
                                "skills": ["Python", "SQL", "Excel", "Power BI", "GenAI", "FastAPI"],
                                "experience_min": 0,
                                "experience_max": 1,
                                "education_required": "MCA / Computer Science / IT",
                                "remote_type": "Hybrid" if "bangalore" in location.lower() else "Remote",
                                "salary_info": "Salary not specified"
                            })
            except Exception as e:
                logger.warning(f"Failed to fetch LinkedIn public jobs for {role}: {e}")

        return jobs
