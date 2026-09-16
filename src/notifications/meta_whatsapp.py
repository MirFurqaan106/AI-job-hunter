import requests
import logging
from typing import Dict, Any
from src.notifications.base import NotificationProvider, ConsoleNotificationProvider

logger = logging.getLogger(__name__)

class MetaWhatsAppCloudAPIProvider(NotificationProvider):
    """
    100% Official Meta WhatsApp Cloud API Provider.
    Free Forever: 1,000 free WhatsApp messages every month directly from Meta.
    """
    def __init__(self, phone_number_id: str, access_token: str, to_phone: str):
        self.phone_number_id = phone_number_id
        self.access_token = access_token
        self.to_phone = to_phone.replace("+", "").replace(" ", "").replace("whatsapp:", "")
        self.console_fallback = ConsoleNotificationProvider()

    def send_job_alert(self, job_data: Dict[str, Any], match_data: Dict[str, Any]) -> bool:
        self.console_fallback.send_job_alert(job_data, match_data)

        if not self.phone_number_id or not self.access_token:
            logger.info("Meta WhatsApp Cloud API credentials missing. Displayed in console.")
            return True

        url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        matched_str = " * ".join(match_data.get("matched_skills", [])) or "None"

        body_text = (
            f"NEW JOB MATCH ({match_data.get('match_score')}%)\n"
            f"Role: {job_data.get('title')}\n"
            f"Company: {job_data.get('company')}\n"
            f"Location: {job_data.get('location')}\n"
            f"Exp: {job_data.get('experience_min')}-{job_data.get('experience_max')} yrs\n"
            f"Skills: {matched_str}\n"
            f"Apply Now: {job_data.get('url')}"
        )

        payload = {
            "messaging_product": "whatsapp",
            "to": self.to_phone,
            "type": "text",
            "text": {
                "preview_url": True,
                "body": body_text
            }
        }

        try:
            res = requests.post(url, headers=headers, json=payload, timeout=10)
            if res.status_code == 200:
                logger.info("Official Meta WhatsApp message sent successfully!")
                return True
            else:
                logger.warning(f"Meta WhatsApp API returned status {res.status_code}: {res.text}")
                return False
        except Exception as e:
            logger.error(f"Error sending message via Meta WhatsApp Cloud API: {e}")
            return False
