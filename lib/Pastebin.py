from .Site import Site
from .Paste import Paste
from . import helper
from time import sleep
from settings import SLEEP_PASTEBIN, SCRAPE_LIMIT
import logging
import requests
import urllib
import json


class PastebinPaste(Paste):
    def __init__(self, id):
        self.id = id
        self.headers = None
        # update pastebin scraping api URL. Must have pastebin pro account to whitelist your IP
        self.url = 'https://scrape.pastebin.com/api_scrape_item.php?i=' + self.id
        super(PastebinPaste, self).__init__()


class Pastebin(Site):
    def __init__(self, last_id=None):
        if not last_id:
            last_id = None
        self.ref_id = last_id
        self.BASE_URL = 'http://pastebin.com'
        self.sleep = SLEEP_PASTEBIN
        self.session = requests.Session()
        super(Pastebin, self).__init__()


    def update(self):
        '''update(self) - Fill Queue with new Pastebin IDs'''
        logging.info('Retrieving Pastebin ID\'s')
        new_pastes = []
        raw = None
        while not raw:
            try:
                raw = urllib.request.urlopen("https://scrape.pastebin.com/api_scraping.php?limit=" + str(SCRAPE_LIMIT))
            except:
                logging.info('Error with pastebin')
                raw = None
                sleep(5)
        # import API result as JSON
        raw_json = json.load(raw)
        #parse json to get keys
        results = []
        #populate results list with paste_ids
        for paste_bulk in raw_json:
            results.append(paste_bulk['key'])
        if not self.ref_id:
            #up to 100 new pastes
            results = results[:100]
        for entry in results:
            paste = PastebinPaste(entry)
            # Check to see if we found our last checked paste_id
            if paste.id == self.ref_id:
                #if paste_id matches last checked id, no more new stuff
                break
            new_pastes.append(paste)
        for entry in new_pastes[::-1]:
            logging.info('Adding URL: ' + entry.url)
            self.put(entry)


    def get_paste_text(self, paste):
        return helper.download(paste.url)
