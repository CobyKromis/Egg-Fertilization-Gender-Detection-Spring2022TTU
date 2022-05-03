from datetime import datetime
import os
import shutil
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
GMAIL_USERNAME = 'eggsorting2022@gmail.com'
GMAIL_PASSWORD = 'eggsortingttu2022'
MAIL_CONTENT = ''
ct = datetime.now()
ctString = ct.strftime("%d/%m/%Y %H:%M:%S")
SUBJECT = 'New Egg Files as of: ' + ctString
SRC = '/home/pi/Desktop/EggDatabase/'
DST = '/home/pi/Desktop/EggDatabase2/'
RECEIVER = "cobykromis@gmail.com"


def update(recipient, subject, content):
    message = MIMEMultipart()
    message['From'] = GMAIL_USERNAME
    message['To'] = recipient
    message['Subject'] = subject
    message.attach(MIMEText(content, 'plain'))

    files = os.listdir(SRC)
    for i in files:
        fileName = os.path.basename(i)
        # print(fileName)
        fileAttach = open(SRC + fileName, 'rb')
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload((fileAttach).read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Disposition', 'attachment', filename=fileName)
        message.attach(payload)

    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.starttls()
    session.login(GMAIL_USERNAME, GMAIL_PASSWORD)
    text = message.as_string()
    session.sendmail(GMAIL_USERNAME, recipient, text)
    session.quit()
    print('Update Sent to: ' + recipient)

    for i in files:
        shutil.move(os.path.join(SRC, i), DST)