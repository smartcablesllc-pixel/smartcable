import re

logos = {
    "Star Plus": "https://upload.wikimedia.org/wikipedia/en/d/d7/StarPlus_Logo.png",
    "Zee TV": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Zee_TV_2025.svg/250px-Zee_TV_2025.svg.png",
    "Colors TV": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Colors_TV_logo.svg/250px-Colors_TV_logo.svg.png",
    "Sony Entertainment": "https://upload.wikimedia.org/wikipedia/en/thumb/d/de/Sony_TV_new.png/250px-Sony_TV_new.png",
    "&amp;TV": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/%26TV_2025.svg/330px-%26TV_2025.svg.png",
    "SAB TV": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/SONY_SAB_SD_Logo_2022.png/250px-SONY_SAB_SD_Logo_2022.png",
    "Star Sports 1": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Star_Sports_Logo_2017.svg/250px-Star_Sports_Logo_2017.svg.png",
    "Star Sports 2": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Star_Sports_Logo_2017.svg/250px-Star_Sports_Logo_2017.svg.png",
    "ESPN": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/ESPN_wordmark.svg/250px-ESPN_wordmark.svg.png",
    "Sony Sports Ten 1": "https://upload.wikimedia.org/wikipedia/en/thumb/c/cd/Sony_Sports_Network.svg/120px-Sony_Sports_Network.svg.png",
    "NDTV 24x7": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/NDTV_247.svg/250px-NDTV_247.svg.png",
    "CNN News18": "https://upload.wikimedia.org/wikipedia/en/thumb/a/ae/CNN-News18.svg/330px-CNN-News18.svg.png",
    "Aaj Tak": "https://upload.wikimedia.org/wikipedia/en/thumb/7/77/Aaj_Tak_logo.svg/250px-Aaj_Tak_logo.svg.png",
    "BBC World News": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/BBC_News_2022_%28Alt%29.svg/250px-BBC_News_2022_%28Alt%29.svg.png",
    "Sony MAX": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/SONY_MAX_Logo_2022.png/250px-SONY_MAX_Logo_2022.png",
    "Zee Cinema": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/Zee_Entertainment_2025.svg/250px-Zee_Entertainment_2025.svg.png",
    "Star Gold": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Star_Gold_Network_logo.png/250px-Star_Gold_Network_logo.png",
    "HBO": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/HBO_logo.svg/250px-HBO_logo.svg.png",
    "Cartoon Network": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Cartoon_Network_2010_logo.svg/250px-Cartoon_Network_2010_logo.svg.png",
    "Nickelodeon": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Nickelodeon_2023_logo_%28outline%29.svg/250px-Nickelodeon_2023_logo_%28outline%29.svg.png",
    "Disney Channel": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/2024_Disney_Channel_text_logo.svg/250px-2024_Disney_Channel_text_logo.svg.png",
    "POGO": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/POGO-logo.png/250px-POGO-logo.png",
    "MTV": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/MTV_2021_%28brand_version%29.svg/250px-MTV_2021_%28brand_version%29.svg.png",
    "VH1": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/VH1_logo.svg/250px-VH1_logo.svg.png",
    "9XM": "https://upload.wikimedia.org/wikipedia/commons/e/ef/9XMHindiMusicTelevisionChannelLogo.jpg",
    "Discovery": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Discovery_Channel_-_Logo_2019.svg/250px-Discovery_Channel_-_Logo_2019.svg.png",
    "National Geographic": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Natgeologo.svg/250px-Natgeologo.svg.png",
    "TLC": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/TLC_logo.svg/250px-TLC_logo.svg.png",
    "History TV18": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/History_%282021%29.svg/250px-History_%282021%29.svg.png"
}

with open("channels.html", "r", encoding="utf-8") as f:
    html = f.read()

def replace_svg(match):
    name = match.group(1).replace("&amp;", "&")
    url = logos.get(name)
    if not url: url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/300px-No_image_available.svg.png"
    
    replacement = f'<div class="channel-card__name">{match.group(1)}</div>'
    
    return replacement

for name_html, url in logos.items():
    # Find the block for the channel
    pattern = r'(<div class="channel-card[^>]*data-channel-name="([^"]+)"[^>]*>.*?<div class="channel-card__icon">\s*)<svg.*?</svg>(\s*</div>)'
    
    def replace_svg_full(match):
        cname = match.group(2)
        if cname == name_html.replace("&amp;", "&"):
            alt_text = f"{cname} Official Logo"
            return match.group(1) + f'<img src="{url}" alt="{alt_text}" class="channel-logo" loading="lazy" width="60" height="60">' + match.group(3)
        return match.group(0)
    
    html = re.sub(pattern, replace_svg_full, html, flags=re.DOTALL)

with open("channels.html", "w", encoding="utf-8") as f:
    f.write(html)
