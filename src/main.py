import sys
import argparse
import logging
import time
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.core.config import load_settings
from src.services.pipeline import JobPipelineService
from src.sources.manual_source import ManualJobSource
from src.notifications.whatsapp import WhatsAppNotificationProvider
from src.notifications.base import ConsoleNotificationProvider

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("AIJobHunter")

def get_notifier(settings):
    if settings.notification.provider == "whatsapp_direct":
        from src.notifications.whatsapp_direct import WhatsAppWebDirectProvider
        return WhatsAppWebDirectProvider(
            phone_number=settings.notification.whatsapp_to or "+917889984798"
        )
    elif settings.notification.provider == "meta":
        from src.notifications.meta_whatsapp import MetaWhatsAppCloudAPIProvider
        return MetaWhatsAppCloudAPIProvider(
            phone_number_id=settings.notification.meta_phone_number_id or "",
            access_token=settings.notification.meta_access_token or "",
            to_phone=settings.notification.whatsapp_to or "+917889984798"
        )
    elif settings.notification.provider == "desktop":
        from src.notifications.desktop import WindowsDesktopNotificationProvider
        return WindowsDesktopNotificationProvider()
    elif settings.notification.provider == "callmebot":
        from src.notifications.whatsapp_free import CallMeBotWhatsAppProvider
        return CallMeBotWhatsAppProvider(
            phone_number=settings.notification.whatsapp_to or "+917889984798",
            api_key=settings.notification.callmebot_api_key or ""
        )
    elif settings.notification.provider == "twilio" and settings.notification.twilio_account_sid:
        return WhatsAppNotificationProvider(
            account_sid=settings.notification.twilio_account_sid,
            auth_token=settings.notification.twilio_auth_token,
            from_number=settings.notification.twilio_whatsapp_from,
            to_number=settings.notification.whatsapp_to
        )
    else:
        return ConsoleNotificationProvider()

def run_pipeline_once(settings):
    logger.info("Starting job discovery pipeline run...")
    notifier = get_notifier(settings)
    service = JobPipelineService(settings, notifier)
    sources = [ManualJobSource()]

    stats = service.process_jobs(sources)
    logger.info(f"Pipeline run completed. Stats: {stats}")
    return stats

def send_test_alert(settings):
    logger.info("Sending test notification...")
    notifier = get_notifier(settings)
    test_job = {
        "title": "Junior Data Analyst",
        "company": "ABC Technologies",
        "location": "Bangalore",
        "experience_min": 0,
        "experience_max": 1,
        "remote_type": "Hybrid",
        "url": "https://example.com/careers/data-analyst-test"
    }
    test_match = {
        "match_score": 95.0,
        "matched_skills": ["Python", "SQL", "Power BI", "Excel"],
        "missing_skills": ["Tableau"],
        "explanation": "Strong match for your MCA profile!"
    }
    notifier.send_job_alert(test_job, test_match)

def main():
    parser = argparse.ArgumentParser(description="AI Job Hunter — 24/7 Personal Job Discovery System")
    parser.add_argument("--once", action="store_true", help="Run job discovery once and exit")
    parser.add_argument("--daemon", action="store_true", help="Run 24/7 background scheduler continuously")
    parser.add_argument("--test-alert", action="store_true", help="Send a instant test alert notification")
    args = parser.parse_args()

    settings = load_settings()

    if args.test_alert:
        send_test_alert(settings)
    elif args.daemon:
        logger.info(f"Launching AI Job Hunter 24/7 Daemon (Interval: {settings.rules.alert_schedule_minutes} mins)")
        while True:
            try:
                run_pipeline_once(settings)
            except Exception as e:
                logger.error(f"Error during scheduled run: {e}")
            time.sleep(settings.rules.alert_schedule_minutes * 60)
    else:
        run_pipeline_once(settings)

if __name__ == "__main__":
    main()
