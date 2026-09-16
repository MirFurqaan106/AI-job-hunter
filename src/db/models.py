from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from src.db.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    company = Column(String, nullable=False, index=True)
    location = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    url = Column(String, unique=True, nullable=False, index=True)
    source = Column(String, default="manual")
    source_job_id = Column(String, nullable=True)
    posted_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    discovered_at = Column(DateTime, default=datetime.utcnow)
    
    experience_min = Column(Integer, default=0)
    experience_max = Column(Integer, default=1)
    education_required = Column(String, nullable=True)
    remote_type = Column(String, default="On-site")
    salary_info = Column(String, default="Salary not specified")
    
    content_hash = Column(String, index=True, nullable=False)
    status = Column(String, default="New") # New, Viewed, Saved, Applied, Skipped, Interview, Rejected
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    matches = relationship("JobMatch", back_populates="job", cascade="all, delete-orphan")

class JobMatch(Base):
    __tablename__ = "job_matches"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    profile_name = Column(String, default="Mir Furqaan Hassan")
    
    match_score = Column(Float, nullable=False)
    matched_skills = Column(JSON, default=[])
    missing_skills = Column(JSON, default=[])
    explanation = Column(Text, nullable=True)
    
    notified = Column(Boolean, default=False)
    notified_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("Job", back_populates="matches")
