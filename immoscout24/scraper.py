import requests
from pyquery import PyQuery as pq



lastid =' '
try:
    with open('lastid.tmp', 'r') as f:
        lastid = f.read().strip()
except:
    pass

resp = requests.get('https://www.immobilienscout24.de/Suche/S-2/Wohnung-Miete/Hamburg/Hamburg')
d = pq(resp.text)
list_items = d('.result-list__listing ')
links = list_items('a[href]')

hrefs = [a.attrib['href'] for a in links]





if hrefs[0] != lastid:
    open('lastid.tmp', 'w').write(hrefs[0])
    print(str("https://www.immobilienscout24.de" + hrefs[0]))
