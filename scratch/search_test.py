import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

try:
    r = requests.get('https://html.duckduckgo.com/html/?q=Apple+TV+4K+site:pisces.bbystatic.com', headers=headers, timeout=5)
    print('DuckDuckGo HTML Status:', r.status_code)
    urls = re.findall(r'https?://[^\s"\'<>]+', r.text)
    images = [u for u in urls if ('bbystatic.com' in u or 'media-amazon' in u) and ('.jpg' in u or '.png' in u)]
    print(f'Found {len(images)} CDN image matches:')
    for img in images[:10]:
        print(' ', img)
except Exception as e:
    print('Error:', e)
