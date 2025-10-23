from fastapi_mail import FastMail, MessageSchema
from app.core.config import config 

async def send_verification_code_to_email(email: str, username: str, code: str):
    message = MessageSchema(
        subject="ITicket Verification",
        recipients=[email],
        body=f"Salom {username}, sizning tasdiqlash kodingiz: {code}",
        subtype="plain"
    )
    fm = FastMail(config.mail_conf)
    await fm.send_message(message)
