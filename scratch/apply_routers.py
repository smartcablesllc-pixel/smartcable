import re

verified_images = {
    'prod-synology-rt6600': 'https://www.synology.com/img/products/detail/RT6600ax/img_og_image.jpg',
    'prod-dlink-ax5400': 'https://aphnetworks.com/article_images/reviews/d-link-dir-x5460/004.jpg',
    'prod-reyee-e5': 'https://eo-sgp-cos.ruijie.com/FU/Upload/Product/2022/6-15/202261539583467.jpg'
}

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

updated = 0
for pid, url in verified_images.items():
    # Match card block and replace img src
    pattern = r'(id="' + re.escape(pid) + r'"[^>]*>.*?<img[^>]*?\ssrc=")([^"]*)(")'
    def repl(m):
        global updated
        updated += 1
        return m.group(1) + url + m.group(3)
    
    html, count = re.subn(pattern, repl, html, count=1, flags=re.DOTALL)
    if count == 0:
        print(f"Warning: pattern did not match for {pid}")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Successfully updated {updated} / {len(verified_images)} router images in index.html!")
