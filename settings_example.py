# settings.py

#MySQL setup
USE_DB = True
DB_HOST = 'localhost' #(or whatever the server IP is)
DB_PORT = 3306
DB_USER = 'pastebin_scraper'
DB_PASS = 'botpassword'
DB_DB = 'paste_db'

# Thresholds
EMAIL_THRESHOLD = 20
HASH_THRESHOLD = 30
DB_KEYWORDS_THRESHOLD = .55

# Time to Sleep for each site
SLEEP_PASTEBIN = 60
SCRAPE_LIMIT = 100

# Other configuration
log_file = "output.log"
PRINT_LOG = True