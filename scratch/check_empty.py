import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

pattern = r'<div class="product-card[^"]*"[^>]*id="([^"]+)"[^>]*>.*?<img[^>]+src="([^"]*)"[^>]*alt="([^"]+)"'
imgs = re.findall(pattern, c, re.DOTALL)
print(f"Total products: {len(imgs)}")
empty = [p for p in imgs if not p[1]]
filled = [p for p in imgs if p[1]]
print(f"Filled images: {len(filled)}")
print(f"Empty images: {len(empty)}")
print("\nProducts needing images:")
for pid, src, name in empty:
    print(f"  {pid:25s} -> {name}")
