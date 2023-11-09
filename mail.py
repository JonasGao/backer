import os
import sys
from email.message import EmailMessage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template


def load_template():
    with open("table.html", "r") as f:
        return Template(f.read())


def main():
    t = load_template()
    body = ""
    for line in sys.stdin:
        body += line

    message = t.substitute(body=body)

    part1 = MIMEText("Repo Report, please see html.", 'plain')
    part2 = MIMEText(message, 'html')

    sender = os.getenv("OUTLOOK_USER")
    recipient = os.getenv("REPORT_RECEIVER")

    email = MIMEMultipart('alternative')
    email["From"] = sender
    email["To"] = recipient
    email["Subject"] = "仓库报告"
    email.attach(part1)
    email.attach(part2)

    smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp.starttls()
    smtp.login(sender, os.getenv("OUTLOOK_KEY"))
    smtp.sendmail(sender, recipient, email.as_string())
    smtp.quit()


if __name__ == '__main__':
    main()
