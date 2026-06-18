import urllib.request
import json
import ssl
import socket
import os
import re
import time

# Patch socket.getaddrinfo to resolve commons.wikimedia.org and upload.wikimedia.org directly
orig_getaddrinfo = socket.getaddrinfo
def patched_getaddrinfo(host, port, *args, **kwargs):
    if host == 'commons.wikimedia.org':
        return orig_getaddrinfo('103.102.166.224', port, *args, **kwargs)
    elif host == 'upload.wikimedia.org':
        return orig_getaddrinfo('103.102.166.240', port, *args, **kwargs)
    return orig_getaddrinfo(host, port, *args, **kwargs)
socket.getaddrinfo = patched_getaddrinfo

channels = {
    "NBC": "File:NBC logo.svg",
    "CBS": "File:CBS logo.svg",
    "ABC": "File:American Broadcasting Company Logo.svg",
    "FOX": "File:Fox Broadcasting Company logo (2019).svg",
    "USA Network": "File:USA Network logo.svg",
    "TBS": "File:TBS logo 2016.svg",
    "ESPN": "File:ESPN wordmark.svg",
    "ESPN2": "File:ESPN2 logo.svg",
    "NBC Sports": "File:NBC Sports 2023.svg",
    "FS1": "File:Fox Sports 1 logo.svg",
    "CNN": "File:CNN.svg",
    "MSNBC": "File:MSNBC 2021-2023.svg",
    "Fox News": "File:Fox News Channel logo.svg",
    "BBC News": "File:BBC News 2022 (Alt).svg",
    "HBO": "File:HBO logo.svg",
    "Showtime": "File:Showtime.svg",
    "Cinemax": "File:Cinemax.svg",
    "Starz": "File:Starz 2022.svg",
    "Cartoon Network": "File:Cartoon Network 2010 logo.svg",
    "Nickelodeon": "File:Nickelodeon 2023 logo (outline).svg",
    "Disney Channel": "File:2024 Disney Channel text logo.svg",
    "Disney XD": "File:Disney XD 2015.svg",
    "MTV": "File:MTV 2021 (brand version).svg",
    "VH1": "File:VH1 logo.svg",
    "Fuse": "File:Fuse logo15.png",
    "Discovery": "File:Discovery Channel - Logo 2019.svg",
    "National Geographic": "File:Natgeologo.svg",
    "TLC": "File:TLC Logo.svg",
    "History Channel": "File:History (2021).svg"
}

output_dir = "images/channels"
os.makedirs(output_dir, exist_ok=True)
context = ssl._create_unverified_context()

print("Starting Commons API queries with retries and delay to prevent rate limiting...")

downloaded_map = {}

# Load existing mapping if it exists
mapping_file = "scratch/logo_mapping.json"
if os.path.exists(mapping_file):
    try:
        with open(mapping_file, "r") as f:
            downloaded_map = json.load(f)
        print(f"Loaded {len(downloaded_map)} existing mappings.")
    except Exception as e:
        print("Failed to load existing mapping:", e)

for name, title in channels.items():
    # Check if we already have this file downloaded and mapped
    target_filename = name.lower().replace(" ", "_").replace("&", "and")
    # We will search if there's any file matching this name in the output directory
    existing_file = None
    for ext in ['.svg', '.png', '.jpg', '.jpeg']:
        if os.path.exists(os.path.join(output_dir, target_filename + ext)):
            existing_file = f"images/channels/{target_filename + ext}"
            break
    
    if existing_file:
        downloaded_map[name] = existing_file
        print(f"Skipping download for {name}, file already exists: {existing_file}")
        continue
        
    safe_title = urllib.parse.quote(title)
    api_url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={safe_title}&prop=imageinfo&iiprop=url&format=json"
    
    # User-agent matching Wikimedia's policy
    headers = {
        'User-Agent': 'SmartCableLogoDownloader/1.0 (admin@smartcablesllc.com; Python urllib)'
    }
    
    retries = 3
    success = False
    
    for attempt in range(retries):
        try:
            print(f"Querying API for {name} (Attempt {attempt+1}/{retries})...")
            req = urllib.request.Request(api_url, headers=headers)
            with urllib.request.urlopen(req, context=context) as response:
                data = json.loads(response.read().decode('utf-8'))
                pages = data.get("query", {}).get("pages", {})
                page_id = list(pages.keys())[0]
                
                if page_id != "-1":
                    img_info = pages[page_id].get("imageinfo", [{}])[0]
                    orig_url = img_info.get("url")
                    if orig_url:
                        # Determine extension
                        ext = os.path.splitext(orig_url)[1].lower()
                        if not ext:
                            ext = ".png" # default fallback
                        
                        filename = target_filename + ext
                        filepath = os.path.join(output_dir, filename)
                        
                        # Download image file
                        print(f"Downloading {name} image from {orig_url}...")
                        time.sleep(1.0) # delay before download
                        img_req = urllib.request.Request(orig_url, headers=headers)
                        with urllib.request.urlopen(img_req, context=context) as img_resp:
                            with open(filepath, 'wb') as f:
                                f.write(img_resp.read())
                        
                        downloaded_map[name] = f"images/channels/{filename}"
                        print(f"Successfully downloaded {name} ({ext}) -> {filepath}")
                        success = True
                        break
                    else:
                        print(f"No original URL found for {name}")
                        break
                else:
                    print(f"Page not found on Commons for {name} ({title})")
                    break
        except Exception as e:
            print(f"Error processing {name} on attempt {attempt+1}: {e}")
            if attempt < retries - 1:
                wait_time = 3 * (attempt + 1)
                print(f"Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)
            else:
                print(f"Failed all attempts for {name}")
        
    time.sleep(1.5) # Sleep between different channels to be polite to Wikimedia

# Write mapping to a JSON file
with open(mapping_file, "w") as f:
    json.dump(downloaded_map, f, indent=2)
print("Finished. Mapping saved to scratch/logo_mapping.json")
