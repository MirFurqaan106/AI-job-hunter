import requests
import xml.etree.ElementTree as ET
import urllib.parse
import re
import logging
from datetime import datetime
from typing import List, Dict, Any
from src.sources.base import JobSource

logger = logging.getLogger(__name__)

class PublicNaukriJobSource(JobSource):
    """
    Ingests public job listings cross-listed on Naukri.com for target roles in India.
    Filters out search index titles and extracts direct job posting links.
    """
    def __init__(self):
        self.search_queries = [
            "Data Analyst Bangalore freshers",
            "Python Developer Bangalore entry level",
            "GenAI Developer India remote",
            "Business Analyst Bangalore 0-1 years",
            "Software Engineer Bangalore MCA"
        ]

    def fetch_jobs(self) -> List[Dict[str, Any]]:
        jobs = []
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }

        for query in self.search_queries:
            try:
                encoded = urllib.parse.quote(query)
                feed_url = f"https://news.google.com/rss/search?q={encoded}+site:naukri.com&hl=en-IN&gl=IN&ceid=IN:en"
                
                res = requests.get(feed_url, headers=headers, timeout=10)
                if res.status_code == 200:
                    root = ET.fromstring(res.text)
                    channel = root.find("channel")
                    if channel is not None:
                        for item in channel.findall("item")[:4]:
                            title = item.findtext("title") or "Naukri Job"
                            link = item.findtext("link") or ""
                            desc = item.findtext("description") or ""

                            # Skip generic search list pages (e.g. "19308 Python Jobs", "Jobs In India")
                            title_lower = title.lower()
                            if any(term in title_lower for term in ["vacancies", "jobseeker's login", "page 5", "jobs in india", "job search"]):
                                continue

                            # Clean company and title
                            company = "Naukri Verified Company"
                            if " - " in title:
                                parts = title.split(" - ")
                                title = parts[0].strip()
                                company = parts[1].strip()

                            # Extract direct Naukri URL if present in description
                            naukri_match = re.search(r'https?://[a-zA-Z0-9\.\-]*naukri\.com/job-listings-[^\s<>"]+', desc)
                            final_url = naukri_match.group(0) if naukri_match else link

                            jobs.append({
                                "title": title,
                                "company": company,
                                "location": "Bangalore / India",
                                "description": f"Naukri Job: {title}. {desc}",
                                "url": final_url,
                                "source": "Naukri Direct Source",
                                "posted_at": datetime.utcnow(),
                                "skills": ["Python", "SQL", "Excel", "Power BI", "Data Analyst"],
                                "experience_min": 0,
                                "experience_max": 1,
                                "education_required": "MCA / CS / IT",
                                "remote_type": "Hybrid",
                                "salary_info": "Salary not specified"
                            })
            except Exception as e:
                logger.warning(f"Failed to fetch Naukri feed for '{query}': {e}")

        return jobs
