import urllib.request
import ssl
import re

url = "https://commons.wikimedia.org/wiki/File:NBC_logo.svg"
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})

try:
    context = ssl._create_unverified_context()
    html = urllib.request.urlopen(req, context=context).read().decode('utf-8')
    matches = re.findall(r'https://upload\.wikimedia\.org/wikipedia/commons/[^\s"\'>]+', html)
    print("Found matches:")
    for m in set(matches):
        print(m)
except Exception as e:
    print("Error:", e)
