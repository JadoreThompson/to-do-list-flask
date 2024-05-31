import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib

def send_email(task, email_recipient):
    load_dotenv('.env')

    email_sender = os.getenv('EMAIL_SENDER')
    email_password = os.getenv('EMAIL_PASSWORD')
    print(email_password)

    subject = 'Task Reminder'
    body = f'You were supposed to {task} today. Don\'t forget to do it!'

    em = EmailMessage()
    em['FROM'] = email_sender
    em['TO'] = email_recipient
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_recipient, em.as_string())

