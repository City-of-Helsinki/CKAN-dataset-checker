# -*- coding: utf-8 -*-
from check_hri_brokenlinks import check_links
from check_hri_expired import check_expired
from email.message import EmailMessage
from email.policy import SMTP
import smtplib
import configparser

conf = configparser.ConfigParser()
conf.read('./default.conf')

# data source and report outfiles
METADATA_URL=conf['DEFAULT']['metadata_url']
NOTFOUND_OUTFILE_NAME = conf['DEFAULT']['notfound_outfile_name']
EXPIRED_OUTFILE_NAME = conf['DEFAULT']['expired_outfile_name']

# mail configuration
# to-list is expected to be comma separated values of the form "Name <email@addre.ss>"
RECIPIENT_LIST = conf['DEFAULT']['recipient_list'].split(',')
SENDER = conf['DEFAULT']['sender']
SERVER = conf['DEFAULT']['server']
TITLE = conf['DEFAULT']['title']
BODY = conf['DEFAULT']['body']

if __name__=='__main__':

    notfound_count = check_links(NOTFOUND_OUTFILE_NAME, METADATA_URL)
    # print 'Not found: ', notfound_count

    expired_count = check_expired(EXPIRED_OUTFILE_NAME, METADATA_URL)
    # print 'Expired: ', expired_count

    msg = EmailMessage()
    msg['Subject'] = TITLE
    msg['From'] = SENDER
    msg['To'] = RECIPIENT_LIST

    msg.set_content(BODY.format(notfound_count, expired_count))

    for file in (NOTFOUND_OUTFILE_NAME, EXPIRED_OUTFILE_NAME):
        with open(file, "rb") as fp:
            report_data = fp.read()
        msg.add_attachment(report_data, maintype="text", subtype="plain")

    with smtplib.SMTP('localhost') as s:
        s.send_message(msg)
