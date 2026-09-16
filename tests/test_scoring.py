from src.core.config import load_settings
from src.engine.scoring import ScoringEngine

def test_high_match_sample_job():
    settings = load_settings()
    scoring = ScoringEngine(settings)

    sample_job = {
        "title": "Junior Data Analyst",
        "company": "Example Tech",
        "location": "Bangalore",
        "description": "Hiring Junior Data Analyst with Python, SQL, Excel, Power BI, Pandas. MCA accepted.",
        "skills": ["Python", "SQL", "Excel", "Power BI", "Pandas"],
        "experience_min": 0,
        "experience_max": 1,
        "education_required": "MCA / Computer Science",
        "remote_type": "Hybrid"
    }

    score, matched, missing, explanation = scoring.calculate_match_score(sample_job)
    
    assert score >= 85.0
    assert "Python" in matched
    assert "SQL" in matched
    assert "Power BI" in matched

def test_unrelated_role_low_match():
    settings = load_settings()
    scoring = ScoringEngine(settings)

    sample_job = {
        "title": "Senior Marketing Manager",
        "company": "Brand Corp",
        "location": "Mumbai",
        "description": "Requires 8 years in SEO, AdWords, Brand Management.",
        "skills": ["SEO", "AdWords"],
        "experience_min": 8,
        "experience_max": 12,
        "education_required": "MBA Marketing",
        "remote_type": "On-site"
    }

    score, matched, missing, explanation = scoring.calculate_match_score(sample_job)
    assert score < 60.0
