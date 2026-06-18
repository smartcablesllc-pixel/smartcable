import urllib.request
import os
import json

channels = {
    "NBC": "nbc.com",
    "CBS": "cbs.com",
    "ABC": "abc.com",
    "FOX": "fox.com",
    "USA Network": "usanetwork.com",
    "TBS": "tbs.com",
    "ESPN": "espn.com",
    "ESPN2": "espn.com", # Fallback to ESPN
    "NBC Sports": "nbcsports.com",
    "FS1": "foxsports.com",
    "CNN": "cnn.com",
    "MSNBC": "msnbc.com",
    "Fox News": "foxnews.com",
    "BBC News": "bbc.com",
    "HBO": "hbo.com",
    "Showtime": "sho.com",
    "Cinemax": "cinemax.com",
    "Starz": "starz.com",
    "Cartoon Network": "cartoonnetwork.com",
    "Nickelodeon": "nick.com",
    "Disney Channel": "disneychannel.com",
    "Disney XD": "disney.com",
    "MTV": "mtv.com",
    "VH1": "vh1.com",
    "Fuse": "fuse.tv",
    "Discovery": "discovery.com",
    "National Geographic": "nationalgeographic.com",
    "TLC": "tlc.com",
    "History Channel": "history.com"
}

# Create output dir
output_dir = "images/channels"
os.makedirs(output_dir, exist_ok=True)

print("Starting downloads...")
for name, domain in channels.items():
    filename = name.lower().replace(" ", "_").replace("&", "and") + ".png"
    filepath = os.path.join(output_dir, filename)
    url = f"https://logo.clearbit.com/{domain}?size=200"
    
    print(f"Downloading logo for {name} ({url}) -> {filepath}")
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    
    try:
        with urllib.request.urlopen(req) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        print(f"Successfully downloaded {name}")
    except Exception as e:
        print(f"Failed to download {name}: {e}")

print("All downloads finished.")
