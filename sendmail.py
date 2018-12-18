# -*- coding: utf-8 -*-
import smtplib
from email.message import EmailMessage

from email.utils import COMMASPACE, formatdate
#from email import Encoders
import os

def send_mail(to, fro, subject, text, files=[],server="localhost"):
    assert type(to)==list
    assert type(files)==list

    msg = EmailMessage()
    msg['From'] = fro
    msg['To'] = COMMASPACE.join(to)
    #msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject.encode('utf-8')

    for file in files:
        with open(file, "rb") as fp:
            file_data = fp.read()
        msg.add_attachment(file_data, maintype="application", subtype="octet-stream")

    with smtplib.SMTP(server) as s:
        s.send_message(msg)

if __name__=='__main__':
    # Example:
    send_mail(['Henri Kotkanen <henri.kotkanen@gmail.com>'],'no-reply <noreply@dev.hel.fi>','Tässä Sinulle, Henri!','Tärkeä viesti Sinulle! Tässä raportti.',['test.txt'])
