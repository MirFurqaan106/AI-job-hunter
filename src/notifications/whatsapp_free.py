import requests
import urllib.parse
import logging
from typing import Dict, Any
from src.notifications.base import NotificationProvider, ConsoleNotificationProvider

logger = logging.getLogger(__name__)

class CallMeBotWhatsAppProvider(NotificationProvider):
    """
    100% FREE WhatsApp notification service via CallMeBot API.
    Zero trial limits, free forever for personal use.
    """
    def __init__(self, phone_number: str, api_key: str):
        # Format phone number: remove '+' or spaces if present
        self.phone = phone_number.replace("+", "").replace(" ", "").replace("whatsapp:", "")
        self.api_key = api_key
        self.console_fallback = ConsoleNotificationProvider()

    def send_job_alert(self, job_data: Dict[str, Any], match_data: Dict[str, Any]) -> bool:
        self.console_fallback.send_job_alert(job_data, match_data)

        if not self.phone or not self.api_key:
            logger.info("CallMeBot API key or phone not provided. Shown in console.")
            return True

        matched_str = " * ".join(match_data.get("matched_skills", [])) or "None"
        missing_str = " * ".join(match_data.get("missing_skills", [])) or "None"

        message_text = (
            f"NEW JOB MATCH ({match_data.get('match_score')}%)\n"
            f"Role: {job_data.get('title')}\n"
            f"Company: {job_data.get('company')}\n"
            f"Location: {job_data.get('location')}\n"
            f"Exp: {job_data.get('experience_min')}-{job_data.get('experience_max')} yrs\n"
            f"Skills: {matched_str}\n"
            f"Apply Link: {job_data.get('url')}"
        )

        encoded_text = urllib.parse.quote(message_text)
        url = f"https://api.callmebot.com/whatsapp.php?phone={self.phone}&text={encoded_text}&apikey={self.api_key}"

        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                logger.info("Free WhatsApp alert sent successfully via CallMeBot!")
                return True
            else:
                logger.warning(f"CallMeBot returned status {res.status_code}: {res.text}")
                return False
        except Exception as e:
            logger.error(f"Error sending WhatsApp alert via CallMeBot: {e}")
            return False
