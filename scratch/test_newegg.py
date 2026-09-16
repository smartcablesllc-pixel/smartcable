import urllib.request
import re

url = 'https://www.newegg.com/d-link-dir-x5460/p/N82E16833127822'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        html = r.read().decode('utf-8', errors='ignore')
        og = re.findall(r'property="og:image"\s+content="([^"]+)"', html)
        if not og:
            og = re.findall(r'content="([^"]+)"\s+property="og:image"', html)
        print('Newegg og:image:', og)
        imgs = re.findall(r'src="([^"]*neweggimages[^"]*)"', html)
        print('Newegg imgs:', imgs[:5])
except Exception as e:
    print('Error:', e)
