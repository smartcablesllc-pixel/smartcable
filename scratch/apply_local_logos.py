import json
import re
import os

# Load mapping
mapping_path = "scratch/logo_mapping.json"
with open(mapping_path, "r") as f:
    mapping = json.load(f)

# Read channels.html
channels_html_path = "channels.html"
with open(channels_html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Let's inspect what data-channel-names exist in channels.html
channel_names_in_html = re.findall(r'data-channel-name="([^"]+)"', html)
print(f"Found {len(channel_names_in_html)} channel cards in HTML.")

# Map data-channel-name in HTML to key in logo_mapping.json
# Let's handle special cases
def get_mapped_logo(html_name):
    # exact match
    if html_name in mapping:
        return mapping[html_name]
    
    # "Fox Sports 1" in HTML vs "FS1" in mapping
    if html_name == "Fox Sports 1" and "FS1" in mapping:
        return mapping["FS1"]
    
    # "History Channel" in HTML vs "History Channel" in mapping (or similar)
    # let's do a case-insensitive check
    for key, val in mapping.items():
        if key.lower() == html_name.lower():
            return val
            
    return None

# Find all channel cards and replace their img src
# Pattern matches:
# <div class="channel-card animate-on-scroll" data-category="entertainment" data-channel-name="NBC">
#   <div class="channel-card__icon">
#     <img src="https://upload.wikimedia.org/..." ...>
#   </div>
# We want to replace the src="..." inside the card.
# To do this safely, let's split the HTML by cards, or use regex with a replacement function.

pattern = r'(<div class="channel-card animate-on-scroll"[^>]*data-channel-name="([^"]+)"[^>]*>.*?<div class="channel-card__icon">\s*<img src=")([^"]+)("[^>]*>\s*</div>)'

replaced_count = 0
not_found = []

def replace_logo_path(match):
    global replaced_count
    prefix = match.group(1)
    html_name = match.group(2)
    old_src = match.group(3)
    suffix = match.group(4)
    
    local_path = get_mapped_logo(html_name)
    if local_path:
        replaced_count += 1
        print(f"Replacing {html_name}: {old_src} -> {local_path}")
        return prefix + local_path + suffix
    else:
        not_found.append(html_name)
        print(f"WARNING: No local logo found for channel name '{html_name}'")
        return match.group(0)

new_html = re.sub(pattern, replace_logo_path, html, flags=re.DOTALL)

if not_found:
    print(f"Could not find local logos for: {not_found}")
else:
    print("All logos successfully resolved!")

# Save updated channels.html
with open(channels_html_path, "w", encoding="utf-8") as f:
    f.write(new_html)

print(f"Replaced {replaced_count} logo paths in channels.html")
