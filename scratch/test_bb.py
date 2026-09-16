import urllib.request
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

def test_search(q):
    url = f"https://www.bestbuy.com/site/searchpage.jsp?st={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            skus = re.findall(r'data-sku-id="(\d+)"', html)
            print(f"{q}: found SKUs: {skus[:5]}")
    except Exception as e:
        print(f"{q}: {e}")

test_search("Synology RT6600ax")
test_search("D-Link EXO AX5400")
test_search("HP Spectre Rechargeable Mouse 700")
