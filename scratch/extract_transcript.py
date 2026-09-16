import re

with open(r'C:\Users\PC\.gemini\antigravity-ide\brain\ce1ce094-d30b-4c60-8753-5516d12c2d91\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# find all media-amazon links with /images/I/
links = set(re.findall(r'https://m\.media-amazon\.com/images/I/[A-Za-z0-9_%+-]+\.(?:jpg|png)', text))
print(f"Total media-amazon links: {len(links)}")
for l in sorted(links):
    print(" ", l)
