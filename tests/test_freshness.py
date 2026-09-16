from datetime import datetime, timedelta
from src.engine.freshness import is_fresh_job

def test_fresh_job_within_24h():
    posted_2h_ago = datetime.utcnow() - timedelta(hours=2)
    assert is_fresh_job(posted_2h_ago, max_age_hours=24) is True

def test_stale_job_older_than_24h():
    posted_25h_ago = datetime.utcnow() - timedelta(hours=25)
    assert is_fresh_job(posted_25h_ago, max_age_hours=24) is False
