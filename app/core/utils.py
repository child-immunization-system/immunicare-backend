# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
# from core.config import settings

# conf = ConnectionConfig(
#     MAIL_USERNAME=settings.MAIL_USERNAME,
#     MAIL_PASSWORD=settings.MAIL_PASSWORD,
#     MAIL_FROM=settings.MAIL_FROM,
#     MAIL_PORT=settings.MAIL_PORT,
#     MAIL_SERVER=settings.MAIL_SERVER,
#     MAIL_TLS=True,
#     MAIL_SSL=False,
#     USE_CREDENTIALS=True,
#     VALIDATE_CERTS=True
# )

# async def send_reset_password_email(email: str, token: str):
#     reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
#     message = MessageSchema(
#         subject="Password Reset Request",
#         recipients=[email],
#         body=f"Please use the following link to reset your password: {reset_url}",
#         subtype="html"
#     )

#     fm = FastMail(conf)
#     await fm.send_message(message)
