import smtplib
import email.message
from concurrent.futures import ThreadPoolExecutor
import asyncio
from .config import Config

_executor = ThreadPoolExecutor(max_workers=4)


def _build_message(subject: str, sender: str, to: str, body: str):
    msg = email.message.EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to
    msg.set_content(body)
    return msg


def send_email_sync(config: Config, subject: str, to: str, body: str):
    msg = _build_message(subject, config.EMAIL_FROM, to, body)
    with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as s:
        if config.SMTP_USER:
            s.login(config.SMTP_USER, config.SMTP_PASSWORD)
        s.send_message(msg)


def send_email_background(config: Config, subject: str, to: str, body: str):
    # dispatch to a thread so API response isn't blocked
    return _executor.submit(send_email_sync, config, subject, to, body)


async def send_email_async(config: Config, subject: str, to: str, body: str):
    # send via thread to avoid blocking event loop
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, send_email_sync, config, subject, to, body)
