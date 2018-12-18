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

    # print "Checking for expired datasets from " + metadata_url
    data = requests.get(metadata_url).json()
    packages = data['result']

    with codecs.open(outfile, 'w', encoding='utf8') as reportfile:

        reportfile.write('url,date_updated,update_frequency\n')
        expired_count = 0
        for package in packages:
            # if package has update information we check do a simple heuristic check
            # and see if has been updated during the last 365 days
            if 'date_updated' in package:
                try:
                    # try in format: 2013-11-10
                    updated = datetime.datetime.strptime(package['date_updated'], '%Y-%m-%d')
                except:
                    # should be in other format: 10/11/2014
                    try:
                        updated = datetime.datetime.strptime(package['date_updated'], '%d/%m/%Y')
                    except: # we never know what the date format is like, huh
                        updated = datetime.datetime.strptime(package['date_updated'], '%m/%d/%Y')

                finally:
                    # check whether the last update was over a year ago
                    if updated and ((datetime.datetime.now() - updated).days) > 365:
                        try:
                            try:
                                update_frequency = package['update_frequency']['fi']
                            except KeyError as e:
                                update_frequency = "update frequency not defined"
                            reportfile.write("{},{},{}\n".format(package['id'], package['date_updated'], update_frequency))
                            expired_count += 1
                        except KeyError as e:
                            print("Data record misshapen while reading update_frequency:")
                            print(e.args)
                            print(package)


        return expired_count
