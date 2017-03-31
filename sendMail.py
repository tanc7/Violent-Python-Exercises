import smtplib
from email.mime.text import MIMEText

def sendMail(user, pwd, to, subject, text):
    msg = MIMEText(text)
    msg['From'] = user
    msg['To'] = to
    msg['Subject'] = Subject
    try:
        return

user = 'username'
pwd = 'password'
sendMail(user, pwd, 'target@tgt.tgt', 'Re: Important', 'Test Message')
