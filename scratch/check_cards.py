import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

cards = re.findall(r'<div class="product-card[^"]*"[^>]*id="([^"]+)"[^>]*>', html)
print('Total cards in index.html:', len(cards))
for c in cards:
    if any(k in c for k in ['router', 'syno', 'dlink', 'reyee', 'wifi', 'tplink', 'asus', 'netgear', 'eero', 'amplifi', 'nest']):
        print(' ', c)
