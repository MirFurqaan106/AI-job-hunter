import sys
from abc import ABC, abstractmethod
from typing import Dict, Any

class NotificationProvider(ABC):
    @abstractmethod
    def send_job_alert(self, job_data: Dict[str, Any], match_data: Dict[str, Any]) -> bool:
        pass

class ConsoleNotificationProvider(NotificationProvider):
    def send_job_alert(self, job_data: Dict[str, Any], match_data: Dict[str, Any]) -> bool:
        matched_str = " • ".join(match_data.get("matched_skills", [])) or "None"
        missing_str = " • ".join(match_data.get("missing_skills", [])) or "None"
        
        message = f"""
[NEW JOB MATCH DETECTED]
----------------------------------
Role:       {job_data.get('title')}
Company:    {job_data.get('company')}
Location:   {job_data.get('location')} ({job_data.get('remote_type', 'On-site')})
Experience: {job_data.get('experience_min')}-{job_data.get('experience_max')} years
Salary:     {job_data.get('salary_info', 'Salary not specified')}
Match Score: {match_data.get('match_score')}%

Matched Skills:
   {matched_str}

Missing/Preferred:
   {missing_str}

AI Summary:
   {match_data.get('explanation')}

[ APPLY NOW ]: {job_data.get('url')}
----------------------------------
"""
        try:
            print(message)
        except UnicodeEncodeError:
            print(message.encode("ascii", errors="replace").decode("ascii"))
        return True
