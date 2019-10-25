import requests
from pyquery import PyQuery as pq


lastid =' '
try:
    with open('lastid.tmp', 'r') as f:
        lastid = f.read().strip()
except:
    pass

resp = requests.get('https://www.wg-gesucht.de/wg-zimmer-in-Hamburg.55.0.0.0.html?offer_filter=1&noDeact=1&city_id=55&category=0&rent_type=0')
d = pq(resp.text)
trs = d('#table-compact-list tr').not_('.inlistTeaser')[2:]
ids = [tr.attrib['adid'] for tr in trs]


if ids[0] != lastid:
    open('lastid.tmp', 'w').write(ids[0])
    print(str("https://www.wg-gesucht.de/" + ids[0]))
