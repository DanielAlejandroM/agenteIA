import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()


class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.hr_email = os.getenv("HR_EMAIL")

    def send_email(self, subject: str, body: str, to_email: str = None):
        recipient = to_email or self.hr_email

        if not all([self.smtp_server, self.smtp_port, self.smtp_user, self.smtp_password, recipient]):
            raise ValueError("Faltan variables SMTP o correo de RRHH.")

        msg = MIMEMultipart()
        msg["From"] = self.smtp_user
        msg["To"] = recipient
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain", "utf-8"))

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.sendmail(self.smtp_user, recipient, msg.as_string())

        return True