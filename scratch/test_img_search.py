import urllib.request
import json
import re

def search_ddg_images(query):
    # DuckDuckGo image search
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }
    url = f"https://duckduckgo.com/?q={urllib.parse.quote(query)}&t=h_&iar=images&iax=images&ia=images"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        
        m = re.search(r'vqd=([\d-]+)&', html)
        if not m:
            m = re.search(r'vqd=\"([\d-]+)\"', html)
        if not m:
            print(f"No vqd for {query}")
            return []
        vqd = m.group(1)
        
        req2 = urllib.request.Request(
            f"https://duckduckgo.com/i.js?l=us-en&o=json&q={urllib.parse.quote(query)}&vqd={vqd}&f=,,,&p=1",
            headers=headers
        )
        with urllib.request.urlopen(req2, timeout=10) as resp2:
            data = json.loads(resp2.read().decode('utf-8'))
            results = data.get('results', [])
            return [r['image'] for r in results[:5]]
    except Exception as e:
        print(f"Error searching {query}: {e}")
        return []

print(search_ddg_images("TiVo Stream 4K streaming media player white background"))
