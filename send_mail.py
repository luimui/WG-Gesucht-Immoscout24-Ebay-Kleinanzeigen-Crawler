import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
load_dotenv()

# Read SMTP credentials from environment variables
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
EMAIL_USER = os.environ.get('EMAIL_USER')
EMAIL_PASS = os.environ.get('EMAIL_PASS')
RECIPIENT = os.environ.get('EMAIL_RECIPIENT')

if not EMAIL_USER or not EMAIL_PASS or not RECIPIENT:
    print("Missing EMAIL_USER, EMAIL_PASS, or EMAIL_RECIPIENT environment variables.")
    sys.exit(1)

subject = sys.argv[1] if len(sys.argv) > 1 else 'No Subject'
body = sys.stdin.read()

msg = MIMEMultipart()
msg['From'] = EMAIL_USER
msg['To'] = RECIPIENT
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)
    server.sendmail(EMAIL_USER, RECIPIENT, msg.as_string())
    server.quit()
    print("Email sent successfully.")
except Exception as e:
    print(f"Failed to send email: {e}")
    sys.exit(2)
