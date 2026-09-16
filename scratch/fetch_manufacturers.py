import urllib.request
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

sites = [
    ('Formuler Z11', 'https://www.formuler.tv/z11promax'),
    ('Xiaomi Mi Box', 'https://www.mi.com/global/product/xiaomi-tv-box-s-2nd-gen/'),
    ('BroadLink RM4 Pro', 'https://www.ibroadlink.com/productinfo/762691.html'),
    ('Ruijie Reyee RG-E5', 'https://www.ruijienetworks.com/products/reyee-wireless/reyee-wireless-routers/rg-e5'),
]

for name, url in sites:
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            og = re.findall(r'property="og:image"\s+content="([^"]+)"', html)
            if not og:
                og = re.findall(r'content="([^"]+)"\s+property="og:image"', html)
            print(f"{name} og:image:", og)
    except Exception as e:
        print(f"{name} error: {e}")
