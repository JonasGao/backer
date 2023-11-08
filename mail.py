import os
import sys
from email.message import EmailMessage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def main():
    table = ("{0: <30}| {1: <25}| {2: <25}| {3: <20}| {4: <6}| {5: <6}| {6}\n"
             .format("repo", "update time", "push time", "default branch", "archived", "disabled"
                     , "message"))
    for line in sys.stdin:
        table += line

    message = f"<html><body><pre><code>{table}<code></pre></body></html>"

    part1 = MIMEText(table, 'plain')
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
