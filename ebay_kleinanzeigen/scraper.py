
import requests
from pyquery import PyQuery as pq
import json
import os
from datetime import datetime, timedelta

ADS_FILE = 'ads_seen.json'
BASE_URL = 'https://www.ebay-kleinanzeigen.de'
URL = BASE_URL + '/s-wohnung-mieten/rostock/c203l137'
TIME_WINDOW_HOURS = 24

# Load seen ads
if os.path.exists(ADS_FILE):
    with open(ADS_FILE, 'r') as f:
        ads_seen = json.load(f)
else:
    ads_seen = {}

now = datetime.now()
time_window = now - timedelta(hours=TIME_WINDOW_HOURS)

resp = requests.get(URL)
d = pq(resp.text)
list_items = d('.ad-listitem').not_('.is-topad')
links = list_items('a[href]')
hrefs = [a.attrib['href'] for a in links]

new_ads = []
for href in hrefs:
    full_url = BASE_URL + href
    # If ad is new or seen within the time window
    ad_time_str = ads_seen.get(full_url)
    ad_time = datetime.fromisoformat(ad_time_str) if ad_time_str else None
    if not ad_time or ad_time < time_window:
        # Mark as seen now
        ads_seen[full_url] = now.isoformat()
        new_ads.append(full_url)

# Save updated ads_seen
with open(ADS_FILE, 'w') as f:
    json.dump(ads_seen, f)


def extract_meta_from_detail(url):
    try:
        resp = requests.get(url)
        d = pq(resp.text)
        title = d('h1').text() or d('.text-module-begin').text() or 'No title'
        price = d('.price-block__value').text() or d('.aditem-main--middle--price-shipping').text() or 'No price'
        location = d('.seller-location').text() or d('.aditem-main--top--left').text() or 'No location'
        date = d('.ad-details__item--date').text() or d('.aditem-main--top--right').text() or 'No date'
        return {
            'title': title.strip(),
            'price': price.strip(),
            'location': location.strip(),
            'date': date.strip(),
            'link': url
        }
    except Exception as e:
        return {'title': 'Error', 'price': '', 'location': '', 'date': '', 'link': url}

if new_ads:
    print("New apartment ads in the last 24 hours:\n")
    rows = []

    for url in new_ads:
        meta = extract_meta_from_detail(url)
        # Try to extract price as integer
        price_str = meta['price'].replace('€', '').replace('.', '').replace(',', '').strip()
        price_val = None
        for part in price_str.split():
            if part.isdigit():
                price_val = int(part)
                break
        if price_val is not None and 350 <= price_val <= 950:
            rows.append(meta)

    headers = ["Title", "Price", "Location", "Date", "Link"]
    col_widths = [40, 15, 20, 18, 200]
    def format_row(row):
        return f"{row['title'][:col_widths[0]].ljust(col_widths[0])} | " \
               f"{row['price'][:col_widths[1]].ljust(col_widths[1])} | " \
               f"{row['location'][:col_widths[2]].ljust(col_widths[2])} | " \
               f"{row['date'][:col_widths[3]].ljust(col_widths[3])} | " \
               f"{row['link'][:col_widths[4]].ljust(col_widths[4])}"

    print(f"{headers[0].ljust(col_widths[0])} | {headers[1].ljust(col_widths[1])} | {headers[2].ljust(col_widths[2])} | {headers[3].ljust(col_widths[3])} | {headers[4].ljust(col_widths[4])}")
    print("-" * (sum(col_widths) + 4*3))
    for row in rows:
        print(format_row(row))
