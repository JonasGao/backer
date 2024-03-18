import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send(subject, message):
    part1 = MIMEText("Repo Report, please see html.", 'plain')
    part2 = MIMEText(message, 'html')

    sender = os.getenv("OUTLOOK_USER")
    recipient = os.getenv("REPORT_RECEIVER")

    if sender is None or recipient is None:
        print("Skip mail sending. Please provide an email address.")
        return

    email = MIMEMultipart('alternative')
    email["From"] = sender
    email["To"] = recipient
    email["Subject"] = subject
    email.attach(part1)
    email.attach(part2)

    smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp.starttls()
    smtp.login(sender, os.getenv("OUTLOOK_KEY"))
    smtp.sendmail(sender, recipient, email.as_string())
    smtp.quit()


if __name__ == '__main__':
    send("Hello")
