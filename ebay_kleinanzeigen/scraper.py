import requests
from pyquery import PyQuery as pq



lastid =' '
try:
    with open('lastid.tmp', 'r') as f:
        lastid = f.read().strip()
except:
    pass

resp = requests.get('https://www.ebay-kleinanzeigen.de/s-auf-zeit-wg/hamburg/c199l9409')
d = pq(resp.text)
list_items = d('.ad-listitem').not_('.is-topad')
links = list_items('a[href]')

hrefs = [a.attrib['href'] for a in links]





if hrefs[0] != lastid:
    open('lastid.tmp', 'w').write(hrefs[0])
    print(str("https://www.ebay-kleinanzeigen.de" + hrefs[0]))
