from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from typing import List, Dict, Any
from sieve.core.config import settings

class EmailDigest:
    """Modern email digest service using SendGrid."""

    def __init__(self):
        self.sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        self.from_email = Email(settings.FROM_EMAIL)

    def format_digest(self, stories: List[Dict[str, Any]]) -> str:
        """Format stories into an HTML email digest."""
        html = "<h2>Today's Top Tech News</h2>\n"
        
        for story in stories:
            html += f"""
            <div style='margin-bottom: 20px;'>
                <h3><a href='{story["url"]}'>{story["title"]}</a></h3>
                <p>Points: {story["points"]} | Comments: {story["num_comments"]}</p>
            </div>
            """
        
        return html

    def send_digest(self, to_email: str, stories: List[Dict[str, Any]]) -> None:
        """Send email digest using SendGrid."""
        html_content = self.format_digest(stories)
        
        message = Mail(
            from_email=self.from_email,
            to_emails=To(to_email),
            subject="Your Daily Tech News Digest",
            html_content=html_content
        )

        try:
            response = self.sg.send(message)
            return response.status_code
        except Exception as e:
            print(f"Error sending email: {e}")
            raise 