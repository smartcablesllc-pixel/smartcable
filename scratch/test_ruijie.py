import urllib.request
import re

url = 'https://reyee.ruijie.com/en-global/products/home-wifi/wifi-router/wifi6-router/rg-ew3200gx-pro/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        html = r.read().decode('utf-8', errors='ignore')
        og = re.findall(r'property="og:image"\s+content="([^"]+)"', html)
        if not og:
            og = re.findall(r'content="([^"]+)"\s+property="og:image"', html)
        print('og:image:', og)
        imgs = re.findall(r'src="([^"]*(?:3200|ew|product|upload)[^"]*\.(?:jpg|png|webp))"', html, re.I)
        print('imgs:', imgs[:5])
except Exception as e:
    print('Error:', e)
