import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

for pid in ['prod-synology-rt6600', 'prod-dlink-ax5400', 'prod-reyee-e5']:
    m = re.search(r'(<div class="product-card[^"]*"[^>]*id="' + pid + r'".*?</div>\s*</div>)', html, re.DOTALL)
    if m:
        print(f"=== {pid} ===")
        print(m.group(1)[:300])
    else:
        print(f"NOT FOUND: {pid}")
