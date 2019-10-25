#Scraper for wg-gesucht, immoscout24, ebay-kleinanzeigen
Scraper that sends emails on new apartment posts

## Installation
Ubuntu:
```
pip install -r requirements.txt
```

To make the trick with mail work you need to config postfix on your machine to make the command `mail` work.
https://www.linode.com/docs/email/postfix/configure-postfix-to-send-mail-using-gmail-and-google-apps-on-debian-or-ubuntu/

## Running
The script scraper executes and extract the last posts from wg-gesucht, immoscout24,ebay-kleinanzeigen one time.


scraper_mailer.sh is running the three scrapers, in a time interval of your choice. It sends an email as soon as a new post is found.
You can exclude any of the given scrapers by simply deleting or commenting out the corresponding lines in scraper_mailer.sh.

Make scraper_mailer.sh executable:
```
chmod +x mailer_scraper.sh
```
And run it:
```
./mailer_scraper.sh
```

