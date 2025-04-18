import smtplib
from email.message import EmailMessage

def send_email(sender: str, recipient: str, subject: str, body: str,
               attachment_path: str, smtp_server: str, smtp_port: int,
               username: str, password: str):
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content(body)

    # Attach PDF file
    with open(attachment_path, "rb") as f:
        file_data = f.read()
        file_name = attachment_path.split("/")[-1]
        msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

    # Send the message
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(username, password)
        server.send_message(msg)