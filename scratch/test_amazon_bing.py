import urllib.request
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def search_amazon_img(query):
    # Search Bing for amazon product page images
    q = f'"{query}" site:amazon.com'
    url = f"https://www.bing.com/images/search?q={urllib.parse.quote(q)}&form=HDRSC2&first=1"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            murls = re.findall(r'murl&quot;:&quot;(https://m\.media-amazon\.com/images/I/[^&]+)&quot;', html)
            return [u for u in murls if not u.endswith('.svg')][:3]
    except Exception as e:
        print(f"Error {query}: {e}")
        return []

test_items = [
    "Xiaomi Mi Box S 4K",
    "Formuler Z11 Pro Max",
    "RCA 3-Device Basic TV Remote RCR313BR",
    "Inteset 4-in-1 Universal Backlit INT-422",
    "Samsung BN59 replacement remote",
    "LG Magic Remote MR20GA",
    "Vizio replacement remote XRT136",
    "Panasonic N2QAYB remote",
    "SofaBaton X1 Universal Remote",
    "BroadLink RM4 Pro Smart Remote",
    "Caavo Control Center",
    "AuviPal G9 Pro Voice Remote",
    "HP Spectre Rechargeable Mouse 700",
    "Lenovo Go Wireless Multi-Device Mouse",
    "eero Pro 6E router",
    "D-Link DIR-X5460 AX5400",
    "Reyee RG-E5 router"
]

for it in test_items:
    res = search_amazon_img(it)
    print(f"=== {it} ===")
    for r in res[:2]:
        print("  ", r)
