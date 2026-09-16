import urllib.request

test_urls = [
    ('panasonic-lz2000', 'https://sk.panasonic.com/wp-content/uploads/2022/10/TX-65LZ2000E_001.jpg'),
    ('inteset-remote', 'https://m.media-amazon.com/images/I/41lbxJUJWjL.jpg'),
    ('lg-magic-basic', 'https://m.media-amazon.com/images/I/71ZX6IUxHkL._SL1500_.jpg'),
    ('vizio-remote', 'https://m.media-amazon.com/images/I/41JCQjrf5fL.jpg'),
    ('hp-spectre700', 'https://m.media-amazon.com/images/I/71XwLX0ySeL.jpg'),
]

for name, u in test_urls:
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = r.read()
            print(f"{name}: {r.status} {r.headers.get('Content-Type')} ({len(data)} bytes)")
    except Exception as e:
        print(f"{name}: ERROR {e}")
