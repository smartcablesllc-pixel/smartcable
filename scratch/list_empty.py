import json
import re

with open('scratch/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

empty_products = []
for p in products:
    pid = p['id']
    m = re.search(r'id="' + re.escape(pid) + r'"[^>]*>.*?<img[^>]+src="([^"]*)"', html, re.DOTALL)
    if m:
        src = m.group(1).strip()
        if not src:
            empty_products.append(p)
    else:
        empty_products.append(p)

print(f"Total empty: {len(empty_products)}")
for p in empty_products:
    print(f"{p['id']:25s} | {p['brand']:15s} | {p['name']:40s} | {p['cat']}")
