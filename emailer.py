import os
import streamlit as st
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Load local .env if exists
load_dotenv()

# Hybrid credential load: st.secrets > .env fallback
EMAIL_ADDRESS = st.secrets.get("EMAIL_ADDRESS", os.getenv("EMAIL_ADDRESS"))
EMAIL_PASSWORD = st.secrets.get("EMAIL_PASSWORD", os.getenv("EMAIL_PASSWORD"))

def send_email(recipient_email, subject, body, attachment_path):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        st.error("Email credentials not found. Please set them in secrets or .env.")
        return

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the body
    msg.attach(MIMEText(body, 'plain'))

    # Attach the PDF file
    with open(attachment_path, 'rb') as f:
        part = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
        part['Content-Disposition'] = f'attachment; filename=\"{os.path.basename(attachment_path)}\"'
        msg.attach(part)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        st.success(f"📤 Report successfully sent to {recipient_email}")
    except Exception as e:
        st.error(f"❌ Failed to send email: {e}")