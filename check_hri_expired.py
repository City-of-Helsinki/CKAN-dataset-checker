#!/usr/bin/python
# -*- coding: UTF-8 -*-

# HRI expiration checker
import requests
import json
import datetime
import codecs

def check_expired(outfile='expired.txt', metadata_url=None):
    if not metadata_url:
        return None

    print "Checking for expired datasets from " + metadata_url
    data = requests.get(metadata_url).json()
    packages = data['packages']

    with codecs.open(outfile, 'w', encoding='utf8') as reportfile:

        reportfile.write('url,date_updated,update_frequency\n')
        expired_count = 0
        for package in packages:
            # check if packages have a specified update frequency and whether they have been updated in the last year
            if (package['extras']['update_frequency']) and (package['extras']['date_updated']):

                try:
                    # try in format: 2013-11-10
                    updated = datetime.datetime.strptime(package['extras']['date_updated'], '%Y-%m-%d')
                except:
                    # should be in other format: 10/11/2014
                    try:
                        updated = datetime.datetime.strptime(package['extras']['date_updated'], '%d/%m/%Y')
                    except: # we never know what the date format is like, huh
                        updated = datetime.datetime.strptime(package['extras']['date_updated'], '%m/%d/%Y')

                finally:
                    # check whether the last update was over a year ago
                    if updated and ((datetime.datetime.now() - updated).days) > 365:
                        reportfile.write(package['ckan_url']+','+package['extras']['date_updated']+','+package['extras']['update_frequency']+'\n')
                        expired_count += 1

        return expired_count
