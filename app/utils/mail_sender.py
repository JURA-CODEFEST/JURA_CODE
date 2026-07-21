## THIS IS ALL FROM SABUHISH.GITHUB.IO/FASTAPI-MAIL DOCS

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List



class EmailSchema(BaseModel):
    email: List[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME = "alokshrestha12386@gmail.com",
    MAIL_PASSWORD = "bclj sfkk yuez nkdw",
    MAIL_FROM = "alokshrestha12386@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="JURA FEDERATION",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


async def verify_email(emails: List[EmailStr],otp):
    html = f"""<p>Hi User,<br> Thanks for wanting to join with us<br>To verify your account, please use the following otp<br> Your OTP is {otp}</p> """

    message = MessageSchema(
        subject="Email verification",
        recipients=emails,
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return {"message": "email has been sent"}

async def forget_password(emails: List[EmailStr],otp):
    html = f"""<p>Hi User,<br>To change your password, please use the following otp<br> Your OTP is {otp}</p> """

    message = MessageSchema(
        subject="Email verification",
        recipients=emails,
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return {"message": "email has been sent"}