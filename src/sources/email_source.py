import imaplib
import email
from email.header import decode_header
import re
import logging
from datetime import datetime
from typing import List, Dict, Any
from src.sources.base import JobSource

logger = logging.getLogger(__name__)

class EmailJobAlertSource(JobSource):
    """
    Ingests job alert emails (e.g. LinkedIn Job Alerts) from a dedicated email inbox.
    """
    def __init__(self, imap_server: str = "", email_user: str = "", email_pass: str = ""):
        self.imap_server = imap_server
        self.email_user = email_user
        self.email_pass = email_pass

    def fetch_jobs(self) -> List[Dict[str, Any]]:
        if not self.imap_server or not self.email_user or not self.email_pass:
            logger.info("IMAP Email credentials not configured. Skipping email ingestion.")
            return []

        jobs = []
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server)
            mail.login(self.email_user, self.email_pass)
            mail.select("inbox")

            # Search for unread job alert emails
            status, messages = mail.search(None, 'UNSEEN SUBJECT "Job Alert"')
            if status != "OK":
                return []

            for num in messages[0].split()[:5]:
                _, data = mail.fetch(num, '(RFC822)')
                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)

                # Extract email body
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/html" or part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode(errors="ignore")
                            break
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore")

                # Extract URLs matching job links
                urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', body)
                job_urls = [u for u in urls if "job" in u.lower() or "career" in u.lower() or "linkedin.com/jobs" in u.lower()]

                if job_urls:
                    jobs.append({
                        "title": "Data Analyst / Developer Alert",
                        "company": "LinkedIn Job Alert",
                        "location": "Bangalore / Remote",
                        "description": body[:500],
                        "url": job_urls[0],
                        "source": "LinkedIn Email Alert",
                        "posted_at": datetime.utcnow(),
                        "skills": ["Python", "SQL", "Data Analyst", "GenAI", "Software Engineer"],
                        "experience_min": 0,
                        "experience_max": 1,
                        "education_required": "MCA / CS",
                        "remote_type": "Remote",
                        "salary_info": "Salary not specified"
                    })

            mail.logout()
        except Exception as e:
            logger.warning(f"Failed to fetch job alert emails: {e}")

        return jobs
