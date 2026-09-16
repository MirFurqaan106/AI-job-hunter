import hashlib
import re
from sqlalchemy.orm import Session
from src.db.models import Job

def generate_content_hash(company: str, title: str, location: str, description: str) -> str:
    """
    Generates a deterministic hash for deduplication based on normalized company, title, location, and description snippet.
    """
    norm_company = re.sub(r'\W+', '', company.lower())
    norm_title = re.sub(r'\W+', '', title.lower())
    norm_location = re.sub(r'\W+', '', location.lower())
    norm_desc = re.sub(r'\W+', '', description[:200].lower())
    
    raw = f"{norm_company}:{norm_title}:{norm_location}:{norm_desc}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def is_duplicate_job(db: Session, url: str, content_hash: str) -> bool:
    """
    Checks if a job with the same URL or content hash already exists in the database.
    """
    existing_url = db.query(Job).filter(Job.url == url).first()
    if existing_url:
        return True
    
    existing_hash = db.query(Job).filter(Job.content_hash == content_hash).first()
    if existing_hash:
        return True
        
    return False
