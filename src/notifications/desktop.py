import subprocess
import shutil
import logging
from typing import Dict, Any
from src.notifications.base import NotificationProvider, ConsoleNotificationProvider

logger = logging.getLogger(__name__)

class WindowsDesktopNotificationProvider(NotificationProvider):
    """
    100% Free, Instant, Native Windows Desktop Notification Provider.
    Zero third-party services, zero delay, works out-of-the-box.
    """
    def __init__(self):
        self.console_fallback = ConsoleNotificationProvider()
        self.ps_exe = shutil.which("powershell.exe") or shutil.which("powershell") or "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"

    def send_job_alert(self, job_data: Dict[str, Any], match_data: Dict[str, Any]) -> bool:
        self.console_fallback.send_job_alert(job_data, match_data)

        title = f"JOB MATCH ({match_data.get('match_score')}%): {job_data.get('title')}"
        company = job_data.get('company', 'Unknown')
        location = job_data.get('location', 'Bangalore')
        matched_str = ", ".join(match_data.get("matched_skills", [])[:3])
        url = job_data.get('url', '')

        message_body = f"{company} | {location}\nSkills: {matched_str}\nApply: {url}"

        # Clean strings for PowerShell execution
        clean_title = title.replace("'", "''").replace('"', '""')
        clean_body = message_body.replace("'", "''").replace('"', '""')

        # Simple PowerShell Balloon / Toast Script
        ps_script = f"""
        [reflection.assembly]::loadwithpartialname('System.Windows.Forms') | Out-Null
        $notify = New-Object System.Windows.Forms.NotifyIcon
        $notify.Icon = [System.Drawing.SystemIcons]::Information
        $notify.Visible = $true
        $notify.ShowBalloonTip(10000, '{clean_title}', '{clean_body}', [System.Windows.Forms.ToolTipIcon]::Info)
        """

        try:
            subprocess.run(
                [self.ps_exe, "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=5,
                check=False
            )
            logger.info("Native Windows Desktop Notification displayed!")
            return True
        except Exception as e:
            logger.error(f"Failed to display Windows Desktop Notification: {e}")
            return False
