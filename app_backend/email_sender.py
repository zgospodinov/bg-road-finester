import os
import smtplib
import ssl
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()

class EmailSender:
    def __init__(self):
        self.email_to = os.getenv("EMAIL_TO")
        self.email_from = os.getenv("EMAIL_FROM")
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT"))
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_pass = os.getenv("SMTP_PASS")
        self.e_uslugi_mvr_url = os.getenv("E_USLUGI_MVR")

    def send_email(self, body, subject="Обобщена проверка на задължения по фиш, НП или споразумение"):
        """
        Sends an HTML email with the provided subject and body.
        The email includes a link to the MVR e-services portal for payment.
        
        Args:
            body (str): The main HTML content of the email.
            subject (str, optional): The subject of the email. Defaults to a summary subject.
        """
        
        print("Sending email notification...")
        content = f"""
        {body}
        <h2>За плащане, при наличие на глоби, посетете:</h2>
        <a href="{self.e_uslugi_mvr_url}">Портал за електронни административни услуги на МВР</a>
        """
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.email_from
        msg['To'] = self.email_to
        msg.add_alternative(content, subtype="html")

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as email_server:
            email_server.login(self.smtp_user, self.smtp_pass)
            email_server.send_message(msg)
        print("Email notification sent")
    
    
    def send_error_email(self, subject="Грешка при проверка на задължения", message=None):
        """
        Sends an error notification email if the data could not be fetched.
        The email includes a message and a link for manual checking.
        
        Args:
            subject (str, optional): The subject of the error email. Defaults to a standard error subject.
            message (str, optional): The HTML message to include in the email. Defaults to a standard error message.
        """
        
        print("Sending error notification email...")
        if message is None:
            message = "<p>Данните за задълженията не бяха успешно извлечени. Моля, проверете в системата или изчакайте следващата насрочена проверка</p>"
        content = f"""
        {message}
        <h2>Ръчна проверка:</h2>
        <a href="{self.e_uslugi_mvr_url}">Портал за електронни административни услуги на МВР</a>
        """
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.email_from
        msg['To'] = self.email_to
        msg.add_alternative(content, subtype="html")

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as email_server:
            email_server.login(self.smtp_user, self.smtp_pass)
            email_server.send_message(msg)
        print("Error notification email sent")