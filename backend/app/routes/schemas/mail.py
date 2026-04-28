from fastapi_mail import FastMail,ConnectionConfig,MessageSchema,MessageType
from .settings import SETTINGS
from pathlib import Path

MAIL_TEMPLATES_FOLDER_PATH = Path(__file__).resolve().parent/"templates/mail"

CONFIG = ConnectionConfig(
    MAIL_USERNAME = SETTINGS.MAIL_USERNAME,
    MAIL_PASSWORD = SETTINGS.MAIL_PASSWORD,
    MAIL_FROM = SETTINGS.MAIL_FROM,
    MAIL_PORT = SETTINGS.MAIL_PORT,
    MAIL_SERVER = SETTINGS.MAIL_SERVER,
    MAIL_FROM_NAME = SETTINGS.MAIL_FROM_NAME,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
    TEMPLATE_FOLDER = MAIL_TEMPLATES_FOLDER_PATH
)

MAIL = FastMail(CONFIG)

async def send_mail_message(recipients:list[str],subject:str,template_body:dict,template_name:str):
    message = MessageSchema(
        recipients=recipients,
        subject=subject,
        template_body=template_body,
        subtype=MessageType.html
    )

    await MAIL.send_message(message,f"{template_name}.html")