import urllib.request
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def search_bing_img(query):
    url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&form=HDRSC2&first=1"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # murl is the direct media url in Bing images
            murls = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', html)
            return murls[:5]
    except Exception as e:
        print(f"Error {query}: {e}")
        return []

items = [
    "Xiaomi Mi Box S 4K white background",
    "Formuler Z11 Pro Max white background",
    "RCA 3-Device Basic TV Remote",
    "Inteset 4-in-1 Universal Backlit INT-422",
    "Sony RM-VLZ620 Universal remote",
    "Samsung Basic Replacement Remote BN59",
    "LG Magic Remote MR20GA",
    "Vizio Universal Replacement Remote XRT136",
    "Panasonic N2QAYB remote",
    "Panasonic LZ2000 OLED TV",
    "Philips OLED+907 TV",
    "SofaBaton X1 Universal Remote",
    "BroadLink RM4 Pro Smart Remote",
    "Caavo Control Center",
    "AuviPal G9 Pro Voice Remote",
    "HP Spectre Rechargeable Mouse 700",
    "Lenovo Go Wireless Multi-Device Mouse",
    "Eero Pro 6E Mesh Router",
    "D-Link EXO AX5400 DIR-X5460",
    "Reyee RG-E5 WiFi 6 Router"
]

for it in items:
    res = search_bing_img(it)
    print(f"=== {it} ===")
    for r in res[:2]:
        print("  ", r)
