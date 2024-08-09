import asyncio
import smtplib
from email.message import EmailMessage

from fastapi import HTTPException
from starlette import status

import config

smtp = smtplib.SMTP(host=config.SMTP_HOST, port=config.SMTP_PORT)


async def init_smtp():
    await asyncio.to_thread(smtp.login, config.SMTP_EMAIL, config.SMTP_PASSWORD)


async def stop_smtp():
    await asyncio.to_thread(smtp.quit)


async def send_email(to: list[str] | str, content: str):
    if isinstance(to, str):
        to = [to]
    if any('\r' in addr or '\n' in addr for addr in to):  # preventing header injection
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='email address can not contain \\r or \\n')
    message = EmailMessage()
    message['From'] = config.SMTP_EMAIL
    message['To'] = ', '.join(to)
    message.set_content(content)
    await asyncio.to_thread(smtp.send_message, message)
