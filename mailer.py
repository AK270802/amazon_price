import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app as app
from config import Config

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = Config.SMTP_USER
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
        server.starttls()
        server.login(Config.SMTP_USER, Config.SMTP_PASS)
        server.send_message(msg)
        server.quit()
        app.logger.info(f"Email sent to {to_email} with subject: {subject}")
    except Exception as e:
        app.logger.warning(f"Failed to send email to {to_email}: {e}")
