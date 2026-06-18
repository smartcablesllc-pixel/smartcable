import urllib.request, re, time, urllib.parse, json

channels = ['Star Plus', 'Zee TV', 'Colors TV', 'Sony Entertainment Television', '&TV', 'Sony SAB', 'Star Sports', 'ESPN', 'Sony Ten', 'NDTV 24x7', 'CNN-News18', 'Aaj Tak', 'BBC News', 'Sony Max', 'Zee Cinema', 'Star Gold', 'HBO', 'Cartoon Network', 'Nickelodeon', 'Disney Channel', 'Pogo (TV channel)', 'MTV', 'VH1', '9XM', 'Discovery Channel', 'National Geographic', 'TLC', 'History (American TV network)']

for c in channels:
    try:
        url = 'https://en.wikipedia.org/wiki/' + urllib.parse.quote(c)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
        match = re.search(r'class="infobox.*?<img.*?src="(//upload\.wikimedia\.org/wikipedia/[^"]+)"', html, re.IGNORECASE | re.DOTALL)
        if match:
            print(c, '->', 'https:' + match.group(1))
        else:
            print(c, '-> NO INFOBOX IMG')
    except Exception as e:
        print(c, '-> ERROR', e)
    time.sleep(0.5)
