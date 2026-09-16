import re
import os

for filename in ['index.html', 'subscribe.html', 'components/navbar.html', 'components/footer.html']:
    if not os.path.exists(filename):
        continue
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    sources = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content)
    missing = [s for s in sources if not os.path.exists(s) and not s.startswith('http')]
    print(filename, f"Total images: {len(sources)}", f"Missing: {len(missing)}")
    if missing:
        for m in missing:
            print(f"  Missing file: {m}")
