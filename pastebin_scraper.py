###############################################################################################################
# Original Author: Jordan Wright
# Modified by: Moez @ CriticalStart
# Version: 1.0
# Usage Example: python pastebin_scraper.py
# Description: This tool monitors Pastebin in real time for data leakage
###############################################################################################################


from lib.regexes import regexes
from lib.Pastebin import Pastebin, PastebinPaste
from time import sleep
from settings import log_file, PRINT_LOG
import threading
import logging
import sys


def monitor():
    '''
    monitor() - Main function... creates and starts threads

    '''
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="more verbose", action="store_true")
    args = parser.parse_args()
    level = logging.INFO
    if args.verbose:
        level = logging.DEBUG
    #logging to both stdout and file
    file_handler = logging.FileHandler(log_file)
    handlers = [file_handler]
    if PRINT_LOG:
        stdout_handler = logging.StreamHandler(sys.stdout)
        handlers.append(stdout_handler)    
    logging.basicConfig(
        level=level,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=handlers
    )
    logging.info('Monitoring...')
    paste_lock = threading.Lock()

    pastebin_thread = threading.Thread(target=Pastebin().monitor, args=[paste_lock])

    # changed threading to not be in a for loop
    # we're only monitoring one site now - Moe
    pastebin_thread.daemon = True
    pastebin_thread.start()

    # Let threads run
    try:
        while(1):
            sleep(5)
    except KeyboardInterrupt:
        logging.warn('Stopped.')


if __name__ == "__main__":
    # banner
    print("""
    ===================================
    PasteBin Scraper
    Originally created by Jordan Wright
    Modified by Moez @ Critical Start
    Version 1.0
    ===================================
    """)
    sleep(5)
    monitor()
