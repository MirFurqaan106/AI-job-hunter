from datetime import datetime, timedelta
from typing import Optional

def is_fresh_job(posted_at: datetime, max_age_hours: int = 24) -> bool:
    """
    Checks if a job was posted within max_age_hours (default 24 hours).
    """
    if not posted_at:
        return False
    cutoff_time = datetime.utcnow() - timedelta(hours=max_age_hours)
    return posted_at >= cutoff_time
