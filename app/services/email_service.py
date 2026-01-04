import logging
from app.core.config import settings

class EmailService:
    @staticmethod
    async def send_otp_email(email: str, otp: str, project_id: str):
        """
        Sends an OTP email. 
        In a real scenario, this would use an SMTP client or an API like SendGrid/AWS SES.
        For this microservice, we'll log it for demonstration.
        """
        logging.info(f"Sending OTP {otp} to {email} for project {project_id}")
        # To simulate sending, we could print to console
        print(f"--- EMAIL SENT ---")
        print(f"To: {email}")
        print(f"Subject: Your Verification Code for {project_id}")
        print(f"Body: Your code is {otp}. It expires in {settings.OTP_EXPIRE_SECONDS // 60} minutes.")
        print(f"------------------")

email_service = EmailService()


