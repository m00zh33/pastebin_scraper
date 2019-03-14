import requests
from time import sleep
import logging

r = requests.Session()

def download(url, headers=None):
    if not headers:
        headers = None
    if headers:
        r.headers.update(headers)
    try:
        response = r.get(url).text
    except requests.ConnectionError:
        logging.warn('[!] Critical Error - Cannot connect to site')
        sleep(5)
        logging.warn('[!] Retrying...')
        response = download(url)
    return response


def run_match(paste):
    interesting = None
    if paste.match():
        interesting = paste.url
        if paste.type == 'db_dump':
            if paste.num_emails > 0:
                interesting = ' Emails: ' + str(paste.num_emails)
            if paste.num_hashes > 0:
                interesting = ' Hashes: ' + str(paste.num_hashes)
            if paste.num_hashes > 0 and paste.num_emails > 0:
                interesting = ' E/H: ' + str(round(
                    paste.num_emails / float(paste.num_hashes), 2))
            interesting = ' Keywords: ' + str(paste.db_keywords)
        elif paste.type == 'google_api':
            interesting = ' Found possible Google API key(s)'
        elif paste.type in ['cisco', 'juniper']:
            interesting = ' Possible ' + paste.type + ' configuration'
        elif paste.type == 'ssh_private':
            interesting = ' Possible SSH private key'
        elif paste.type == 'honeypot':
            interesting = ' Honeypot Log'
        elif paste.type == 'pgp_private':
            interesting = ' Found possible PGP Private Key'
    return interesting
