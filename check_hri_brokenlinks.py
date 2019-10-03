# encoding: utf-8
import os
import sys
from urllib.request import urlopen
import urllib.request, urllib.error, urllib.parse
import urllib.parse
import json
import socket

# From the werkzeug-project: https://github.com/mitsuhiko/werkzeug/blob/master/werkzeug/urls.py
def url_fix(s, charset='utf-8'):
    """Sometimes you get an URL by a user that just isn't a real
    URL because it contains unsafe characters like ' ' and so on.  This
    function can fix some of the problems in a similar way browsers
    handle data entered by the user:

    >>> url_fix(u'http://de.wikipedia.org/wiki/Elf (Begriffsklärung)')
    'http://de.wikipedia.org/wiki/Elf%20%28Begriffskl%C3%A4rung%29'

    :param charset: The target charset for the URL if the url was
                    given as unicode string.
    """
#    if isinstance(s, str):
#        s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urllib.parse.urlsplit(s)
    path = urllib.parse.quote(path, '/%')
    qs = urllib.parse.quote_plus(qs, ':&=')
    return urllib.parse.urlunsplit((scheme, netloc, path, qs, anchor))

def iterate_resources(packages):
    for package in packages:
        for resource in package['resources']:
            url = url_fix(resource['url'])
            yield dict(package=package, url=url)

def load_metadata(url):
    metadata = json.load(urlopen(url))
    packages = metadata['result']
    return list(iterate_resources(packages))

def check_links(outfile='notfound.txt', metadata_url=None):
    if not metadata_url:
        return None

    print("Checking for broken links from " + metadata_url)
    notfound_count = 0

    resources = load_metadata(metadata_url)
    notfound = open(outfile, 'w') # just overwrite it
    for resource in resources:
        package_name = resource['package']['name']
        url = resource['url']
        try:
            data = urlopen(url, timeout=5)

        except urllib.error.HTTPError as e:
            notfound.write(f"{e.reason} at {url}, from {package_name}\n")
            notfound_count += 1
            continue

        except urllib.error.URLError as e:
            notfound.write(f"Something went wrong at {url}, from {package_name}\n")
            notfound_count += 1
            continue

        except socket.timeout as e:
            notfound.write(f"Connection timed out at {url}, from {package_name}\n")
            continue

        except Exception as e:
            print(vars(e))
            print(type(e))
            notfound.write(f"Error: {e}, at {url}, from {package_name}\n")
            notfound_count += 1
            continue

    notfound.close()
    return notfound_count
