import urllib.parse
import webbrowser
import logging
from typing import Dict, Any
from src.notifications.base import NotificationProvider, ConsoleNotificationProvider

logger = logging.getLogger(__name__)

class WhatsAppWebDirectProvider(NotificationProvider):
    """
    100% Free WhatsApp Direct Web Link Provider.
    Opens WhatsApp Web / WhatsApp App directly on your PC with the pre-filled job alert message.
    Zero API keys, zero third-party servers, 100% Free Forever.
    """
    def __init__(self, phone_number: str):
        self.phone = phone_number.replace("+", "").replace(" ", "").replace("whatsapp:", "")
        self.console_fallback = ConsoleNotificationProvider()

    def send_job_alert(self, job_data: Dict[str, Any], match_data: Dict[str, Any]) -> bool:
        self.console_fallback.send_job_alert(job_data, match_data)

        matched_str = " * ".join(match_data.get("matched_skills", [])) or "None"

        message_text = (
            f"🔔 *NEW JOB MATCH ({match_data.get('match_score')}%)*\n\n"
            f"🎯 *Role*: {job_data.get('title')}\n"
            f"🏢 *Company*: {job_data.get('company')}\n"
            f"📍 *Location*: {job_data.get('location')}\n"
            f"💼 *Exp*: {job_data.get('experience_min')}-{job_data.get('experience_max')} yrs\n"
            f"🧠 *Skills*: {matched_str}\n\n"
            f"👉 *Apply Now*: {job_data.get('url')}"
        )

        encoded_text = urllib.parse.quote(message_text)
        wa_url = f"https://api.whatsapp.com/send?phone={self.phone}&text={encoded_text}"

        try:
            logger.info(f"Opening WhatsApp Web chat directly for {self.phone}...")
            webbrowser.open(wa_url)
            return True
        except Exception as e:
            logger.error(f"Failed to open WhatsApp Web link: {e}")
            return False
