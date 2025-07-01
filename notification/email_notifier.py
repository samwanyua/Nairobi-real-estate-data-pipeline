import smtplib
from email.mime.text import MIMEText

def send_email_alert():
    sender = "samexample8@gmail.com"
    recipient = "sam2wanyua@gmail.com"
    subject = "New Property Alert"
    body = "A new 3-bedroom listing in Westlands is available for KES 90,000/month."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    with smtplib.SMTP("mailserver", 587) as server:
        server.starttls()
        server.login("admin", "admin")
        server.sendmail(sender, recipient, msg.as_string())
