import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to find each product card and replace its image src
# Card pattern:
# <div class="product-card..." ... id="prod-XYZ">
# ...
# <img class="product-card__img" src="..." alt="..." loading="lazy">

pattern = re.compile(
    r'(<div class="product-card[^"]*"[^>]*id="(prod-[^"]+)"[^>]*>[\s\S]*?<div class="product-card__image-wrap">[\s\S]*?<img class="product-card__img"\s+)src="[^"]+"',
    re.MULTILINE
)

def replacer(m):
    prefix = m.group(1)
    prod_id = m.group(2)
    return f'{prefix}src="images/products/{prod_id}.jpg"'

new_content, count = pattern.subn(replacer, content)

print(f"Replaced {count} product image sources in index.html")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
