import logging
from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from src.core.config import Settings
from src.db.database import SessionLocal, init_db
from src.db.models import Job, JobMatch
from src.engine.freshness import is_fresh_job
from src.engine.deduplicator import generate_content_hash, is_duplicate_job
from src.engine.scoring import ScoringEngine
from src.sources.base import JobSource
from src.notifications.base import NotificationProvider

logger = logging.getLogger(__name__)

class JobPipelineService:
    def __init__(self, settings: Settings, notification_provider: NotificationProvider):
        self.settings = settings
        self.scoring_engine = ScoringEngine(settings)
        self.notification_provider = notification_provider
        init_db()

    def process_jobs(self, sources: List[JobSource]) -> Dict[str, int]:
        stats = {
            "total_collected": 0,
            "rejected_stale": 0,
            "rejected_duplicate": 0,
            "processed": 0,
            "high_matches": 0,
            "alerts_sent": 0
        }

        db: Session = SessionLocal()
        try:
            for source in sources:
                raw_jobs = source.fetch_jobs()
                stats["total_collected"] += len(raw_jobs)

                for job_dict in raw_jobs:
                    posted_at = job_dict.get("posted_at", datetime.utcnow())
                    
                    # 1. Freshness Check (<= 24 hours)
                    if not is_fresh_job(posted_at, self.settings.rules.max_job_age_hours):
                        logger.info(f"Skipping stale job (>24h): {job_dict.get('title')} - Posted: {posted_at}")
                        stats["rejected_stale"] += 1
                        continue

                    # 2. Content Hashing & Deduplication
                    title = job_dict.get("title", "Unknown Title")
                    company = job_dict.get("company", "Unknown Company")
                    location = job_dict.get("location", "Location Not Specified")
                    description = job_dict.get("description", "")
                    url = job_dict.get("url", "")

                    content_hash = generate_content_hash(company, title, location, description)

                    if is_duplicate_job(db, url, content_hash):
                        logger.info(f"Skipping duplicate job: {title} at {company}")
                        stats["rejected_duplicate"] += 1
                        continue

                    # 3. Transparent Match Scoring
                    score, matched_skills, missing_skills, explanation = self.scoring_engine.calculate_match_score(job_dict)
                    stats["processed"] += 1

                    # 4. Store in Database
                    db_job = Job(
                        title=title,
                        company=company,
                        location=location,
                        description=description,
                        url=url,
                        source=job_dict.get("source", "unknown"),
                        posted_at=posted_at,
                        experience_min=job_dict.get("experience_min", 0),
                        experience_max=job_dict.get("experience_max", 1),
                        education_required=job_dict.get("education_required"),
                        remote_type=job_dict.get("remote_type", "On-site"),
                        salary_info=job_dict.get("salary_info", "Salary not specified"),
                        content_hash=content_hash,
                        status="New"
                    )
                    db.add(db_job)
                    db.commit()
                    db.refresh(db_job)

                    # Store Match Record
                    is_high_match = score >= self.settings.rules.min_match_score_for_alert
                    db_match = JobMatch(
                        job_id=db_job.id,
                        profile_name=self.settings.candidate.name,
                        match_score=score,
                        matched_skills=matched_skills,
                        missing_skills=missing_skills,
                        explanation=explanation,
                        notified=False
                    )
                    db.add(db_match)
                    db.commit()
                    db.refresh(db_match)

                    if is_high_match:
                        stats["high_matches"] += 1
                        match_payload = {
                            "match_score": score,
                            "matched_skills": matched_skills,
                            "missing_skills": missing_skills,
                            "explanation": explanation
                        }
                        sent = self.notification_provider.send_job_alert(job_dict, match_payload)
                        if sent:
                            db_match.notified = True
                            db_match.notified_at = datetime.utcnow()
                            db.commit()
                            stats["alerts_sent"] += 1

        finally:
            db.close()

        return stats
