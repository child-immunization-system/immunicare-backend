from fastapi_mail import FastMail, MessageSchema
from core.config import settings

class NotificationService:
    def __init__(self):
        self.mail = FastMail(settings)

    async def send_notification(self, email: str, subject: str, body: str):
        message = MessageSchema(
            subject=subject,
            recipients=[email],
            body=body,
            subtype="html"
        )
        await self.mail.send_message(message)
