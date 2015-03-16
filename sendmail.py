# -*- coding: utf-8 -*-
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import os

def send_mail(to, fro, subject, text, files=[],server="localhost"):
    assert type(to)==list
    assert type(files)==list

    msg = MIMEMultipart()
    msg['From'] = fro
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject.encode('utf-8')

    msg.attach( MIMEText(text.encode('utf-8')) )

    for file in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(file,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                       % os.path.basename(file))
        msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.sendmail(fro, to, msg.as_string() )
    smtp.close()

if __name__=='__main__':
    # Example:
    send_mail(['Henri Kotkanen <henri.kotkanen@gmail.com>'],'no-reply <noreply@dev.hel.fi>','Tässä Sinulle, Henri!','Tärkeä viesti Sinulle! Tässä raportti.',['test.txt'])
