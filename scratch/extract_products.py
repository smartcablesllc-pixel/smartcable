import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

cards = text.split('<div class="product-card animate-on-scroll"')[1:]
print(f"Total card chunks: {len(cards)}")

products = []
for i, chunk in enumerate(cards):
    chunk = chunk.split('<!-- Product Card')[0].split('<!-- =')[0]
    cat_match = re.search(r'data-category="([^"]+)"', chunk)
    id_match = re.search(r'id="([^"]+)"', chunk)
    img_match = re.search(r'<img[^>]+class="product-card__img"[^>]*src="([^"]+)"[^>]*alt="([^"]+)"', chunk)
    if not img_match:
        img_match = re.search(r'<img[^>]+src="([^"]+)"[^>]*alt="([^"]+)"', chunk)
    brand_match = re.search(r'<div class="product-card__brand">([^<]+)</div>', chunk)
    name_match = re.search(r'<div class="product-card__name">([^<]+)</div>', chunk)
    price_match = re.search(r'<div class="product-card__price">([^<]+)</div>', chunk)

    cat = cat_match.group(1) if cat_match else ""
    pid = id_match.group(1) if id_match else ""
    src = img_match.group(1) if img_match else ""
    alt = img_match.group(2) if img_match else ""
    brand = brand_match.group(1).strip() if brand_match else ""
    name = name_match.group(1).strip() if name_match else ""
    price = price_match.group(1).strip() if price_match else ""

    products.append({
        'index': i + 1,
        'cat': cat,
        'id': pid,
        'src': src,
        'alt': alt,
        'brand': brand,
        'name': name,
        'price': price
    })
    print(f"{i+1:2d}. [{cat:16s}] ID: {pid:22s} | {brand:12s} | {name} | {price}")

import json
with open('scratch/products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, indent=2)
print("Saved to scratch/products.json")
