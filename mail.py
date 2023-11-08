import os
import sys
from email.message import EmailMessage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

T = "{0: <30}| {1: <25}| {2: <25}| {3: <20}| {4: <10}| {5: <10}| {6: <20}| {7: <25}| {8: <10}| {9: <25}| {10}\n"


def main():
    table = (T.format(
        "repo",  # 0
        "update time",  # 1
        "push time",  # 2
        "default branch",  # 3
        "archived",  # 4
        "disabled",  # 5
        "tag name",  # 6
        "tag time",  # 7
        "commit sha",  # 8
        "commit time",  # 9
        "message"  # 10
    ))
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
