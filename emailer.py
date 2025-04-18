import os
import streamlit as st
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Load from .env for local dev
load_dotenv()

EMAIL_ADDRESS = st.secrets.get("EMAIL_ADDRESS", os.getenv("EMAIL_ADDRESS"))
EMAIL_PASSWORD = st.secrets.get("EMAIL_PASSWORD", os.getenv("EMAIL_PASSWORD"))


def send_email(recipient_email, subject, body, attachment_path):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        st.error("❌ Email credentials not found. Set them in Streamlit secrets or .env.")
        return

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with open(attachment_path, 'rb') as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
            msg.attach(part)
    except Exception as file_err:
        st.error(f"❌ Failed to attach PDF: {file_err}")
        return

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        st.success(f"📤 Report successfully sent to {recipient_email}")
    except smtplib.SMTPAuthenticationError:
        st.error("❌ Authentication failed. Check your app password or Gmail security settings.")
    except smtplib.SMTPRecipientsRefused:
        st.error("❌ Email was rejected. Double-check the recipient address.")
    except Exception as e:
        st.error(f"❌ Failed to send email: {e}")