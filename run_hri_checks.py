#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from check_hri_brokenlinks import check_links
from check_hri_expired import check_expired
from email.message import EmailMessage
from email import policy
from datetime import date
import os

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
TITLE = conf['DEFAULT']['title']
BODY = conf['DEFAULT']['body']

if __name__=='__main__':

    notfound_count = check_links(NOTFOUND_OUTFILE_NAME, METADATA_URL)
    expired_count = check_expired(EXPIRED_OUTFILE_NAME, METADATA_URL)

    msg = EmailMessage(policy=policy.SMTP)
    msg['Subject'] = TITLE
    msg['From'] = SENDER
    msg['To'] = RECIPIENT_LIST

    msg.set_content(BODY.format(notfound_count=notfound_count, expired_count=expired_count))

    for file in (NOTFOUND_OUTFILE_NAME, EXPIRED_OUTFILE_NAME):
        with open(file, "rb") as fp:
            report_data = fp.read()
        name, extension = os.path.splitext(file)
        filename = f"{name}_{date.today().strftime('%Y%m%d')}{extension}"
        msg.add_attachment(report_data, filename=filename, maintype="text", subtype="plain", disposition="inline")

    if conf.has_option('', 'smtp_server'):
        with smtplib.SMTP(conf['DEFAULT']['smtp_server']) as s:
            if conf.has_option('', 'smtp_user'):
                s.login(conf['DEFAULT']['smtp_user'], conf['DEFAULT']['smtp_pass'])
            s.send_message(msg)
    else:
        print("smtp_server not set, outputting message in dummy mode")
        print(msg.as_string())
