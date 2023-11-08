import os
import sys
from email.message import EmailMessage
import smtplib


def main():
    message = ("{0: <30}| {1: <25}| {2: <25}| {3: <20}| {4}\n"
               .format("repo", "update time", "push time", "default branch", "message"))
    for line in sys.stdin:
        message += line

    sender = os.getenv("OUTLOOK_USER")
    recipient = os.getenv("REPORT_RECEIVER")

    email = EmailMessage()
    email["From"] = sender
    email["To"] = recipient
    email["Subject"] = "仓库报告"
    email.set_content(message)

    smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp.starttls()
    smtp.login(sender, os.getenv("OUTLOOK_KEY"))
    smtp.sendmail(sender, recipient, email.as_string())
    smtp.quit()


if __name__ == '__main__':
    main()
