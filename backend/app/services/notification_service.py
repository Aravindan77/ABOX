"""
Notification Service - Sends email notifications via SMTP.
Falls back silently when SMTP is not configured.
"""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from app.core.config import settings

logger = logging.getLogger(__name__)


class NotificationService:
    def _is_configured(self) -> bool:
        return bool(settings.SMTP_HOST and settings.SMTP_USER and settings.SMTP_PASS)

    def _send(self, to: str, subject: str, html_body: str) -> bool:
        if not self._is_configured():
            logger.info(f"[Notifications] SMTP not configured – skipping: {subject}")
            return False
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = settings.SMTP_USER
            msg["To"] = to
            msg.attach(MIMEText(html_body, "html"))
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.ehlo()
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASS)
                server.sendmail(settings.SMTP_USER, to, msg.as_string())
            return True
        except Exception as e:
            logger.error(f"[Notifications] Failed to send email: {e}")
            return False

    def notify_submission_received(self, researcher_email: str, bug_id: str, title: str) -> bool:
        subject = f"Bug Report Received – #{bug_id[:8]}"
        html = f"""
        <h2>Your Bug Report Has Been Received</h2>
        <p><b>Title:</b> {title}</p>
        <p><b>ID:</b> {bug_id}</p>
        <p>Our AI engine is analyzing your submission. You'll hear back shortly.</p>
        <br><p>— Anti-Gravity Bug Bounty Team</p>
        """
        return self._send(researcher_email, subject, html)

    def notify_approved(self, researcher_email: str, bug_id: str, bounty_matic: float, tx_hash: Optional[str]) -> bool:
        subject = f"🎉 Bug Approved & Bounty Sent – #{bug_id[:8]}"
        html = f"""
        <h2>Your Bug Report Was Approved!</h2>
        <p><b>Bounty:</b> {bounty_matic} MATIC</p>
        <p><b>Transaction:</b> {tx_hash or "N/A"}</p>
        <p>Well done! Your trust score has been updated.</p>
        <br><p>— Anti-Gravity Bug Bounty Team</p>
        """
        return self._send(researcher_email, subject, html)

    def notify_rejected(self, researcher_email: str, bug_id: str, reason: str) -> bool:
        subject = f"Bug Report Reviewed – #{bug_id[:8]}"
        html = f"""
        <h2>Bug Report Status Update</h2>
        <p>Unfortunately your recent submission was not accepted.</p>
        <p><b>Reason:</b> {reason}</p>
        <p>Keep hunting! We hope to see more reports from you.</p>
        <br><p>— Anti-Gravity Bug Bounty Team</p>
        """
        return self._send(researcher_email, subject, html)

    def notify_new_bug_to_admin(self, admin_email: str, bug_id: str, title: str, severity: str, ai_score: float) -> bool:
        subject = f"[{severity.upper()}] New Bug Needs Review – #{bug_id[:8]}"
        html = f"""
        <h2>New Bug Report Requires Human Review</h2>
        <p><b>Title:</b> {title}</p>
        <p><b>Severity:</b> {severity}</p>
        <p><b>AI Confidence:</b> {ai_score:.0%}</p>
        <p><b>ID:</b> {bug_id}</p>
        <br><p>— Anti-Gravity Bug Bounty Platform</p>
        """
        return self._send(admin_email, subject, html)


notification_service = NotificationService()
