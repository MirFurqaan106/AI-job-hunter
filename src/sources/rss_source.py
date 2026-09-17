import requests
import xml.etree.ElementTree as ET
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
from src.sources.base import JobSource

logger = logging.getLogger(__name__)

class PublicRSSJobSource(JobSource):
    """
    Fetches real live job postings from public job feeds & permitted tech job RSS endpoints.
    """
    def __init__(self):
        self.feed_urls = [
            "https://remotive.com/remote-jobs/feed",
            "https://jobspress.io/feed/",
            "https://weworkremotely.com/categories/remote-programming-jobs.rss"
        ]

    def parse_rss_item(self, item: ET.Element, source_name: str) -> Dict[str, Any]:
        title = item.findtext("title") or "Unknown Title"
        link = item.findtext("link") or ""
        desc = item.findtext("description") or ""
        pub_date_str = item.findtext("pubDate") or ""

        # Parse pubDate or fallback to now
        posted_at = datetime.utcnow()
        if pub_date_str:
            try:
                from email.utils import parsedate_to_datetime
                posted_at = parsedate_to_datetime(pub_date_str).replace(tzinfo=None)
            except Exception:
                posted_at = datetime.utcnow()

        company = "Tech Company"
        if " - " in title:
            parts = title.split(" - ")
            title = parts[0].strip()
            company = parts[1].strip()
        elif " at " in title:
            parts = title.split(" at ")
            title = parts[0].strip()
            company = parts[1].strip()

        return {
            "title": title,
            "company": company,
            "location": "Remote / India",
            "description": desc,
            "url": link,
            "source": source_name,
            "posted_at": posted_at,
            "skills": ["Python", "SQL", "Data Analyst", "Software Engineer", "GenAI"],
            "experience_min": 0,
            "experience_max": 1,
            "education_required": "MCA / Computer Science",
            "remote_type": "Remote",
            "salary_info": "Salary not specified"
        }

    def fetch_jobs(self) -> List[Dict[str, Any]]:
        jobs = []
        for url in self.feed_urls:
            try:
                res = requests.get(url, timeout=10, headers={"User-Agent": "AIJobHunter/1.0"})
                if res.status_code == 200:
                    root = ET.fromstring(res.text)
                    channel = root.find("channel")
                    if channel is not None:
                        for item in channel.findall("item")[:10]:
                            job = self.parse_rss_item(item, source_name="Public Tech RSS")
                            jobs.append(job)
            except Exception as e:
                logger.warning(f"Failed to fetch RSS jobs from {url}: {e}")
        return jobs
