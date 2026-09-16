import logging
from src.notifications.base import NotificationProvider, ConsoleNotificationProvider
from typing import Dict, Any

logger = logging.getLogger(__name__)

class WhatsAppNotificationProvider(NotificationProvider):
    def __init__(self, account_sid: str, auth_token: str, from_number: str, to_number: str):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_number = from_number
        self.to_number = to_number
        self.console_fallback = ConsoleNotificationProvider()

        if account_sid and auth_token:
            try:
                from twilio.rest import Client
                self.client = Client(account_sid, auth_token)
            except Exception as e:
                logger.warning(f"Failed to initialize Twilio client: {e}. Falling back to console output.")
                self.client = None
        else:
            self.client = None

    def send_job_alert(self, job_data: Dict[str, Any], match_data: Dict[str, Any]) -> bool:
        # Print to console as well
        self.console_fallback.send_job_alert(job_data, match_data)

        if not self.client:
            logger.info("Twilio credentials not configured. Displayed notification in console.")
            return True

        matched_str = " • ".join(match_data.get("matched_skills", [])) or "None"
        missing_str = " • ".join(match_data.get("missing_skills", [])) or "None"

        body = (
            f"🔔 *NEW JOB MATCH*\n\n"
            f"*{job_data.get('title')}*\n"
            f"🏢 Company: {job_data.get('company')}\n"
            f"📍 Location: {job_data.get('location')}\n"
            f"💼 Experience: {job_data.get('experience_min')}–{job_data.get('experience_max')} years\n"
            f"🎯 Match: *{match_data.get('match_score')}%*\n\n"
            f"🧠 Skills: {matched_str}\n"
            f"⚠️ Missing: {missing_str}\n\n"
            f"👉 *APPLY NOW*: {job_data.get('url')}"
        )

        try:
            message = self.client.messages.create(
                body=body,
                from_=self.from_number,
                to=self.to_number
            )
            logger.info(f"WhatsApp alert sent successfully! Message SID: {message.sid}")
            return True
        except Exception as e:
            logger.error(f"Failed to send WhatsApp message via Twilio: {e}")
            return False
