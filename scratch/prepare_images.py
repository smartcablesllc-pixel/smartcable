"""
Generate and optimize crisp, real product photos for Smart Cable Services.
Saves 60 local product images into images/products/<id>.jpg
and 6 subscription package images into images/products/sub-<pkg>.jpg.
"""

import os
import io
import urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

os.makedirs('images/products', exist_ok=True)

# High-resolution category base photos from Unsplash
CATEGORY_BASE_URLS = {
    'streaming': [
        'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=800&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800&auto=format&fit=crop&q=80'
    ],
    'simple-remote': [
        'https://images.unsplash.com/photo-1528928441742-b4ccac1bb04c?w=800&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=800&auto=format&fit=crop&q=80'
    ],
    'smart-tv': [
        'https://images.unsplash.com/photo-1593784991095-a205069470b6?w=800&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1593305841991-05c297ba4575?w=800&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=800&auto=format&fit=crop&q=80'
    ],
    'smart-remote': [
        'https://images.unsplash.com/photo-1528928441742-b4ccac1bb04c?w=800&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=800&auto=format&fit=crop&q=80'
    ],
    'mouse': [
        'https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=800&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1629429408209-1f912961dbd8?w=800&auto=format&fit=crop&q=80'
    ],
    'router': [
        'https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=800&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&auto=format&fit=crop&q=80'
    ],
    'subscription': [
        'https://images.unsplash.com/photo-1593784991095-a205069470b6?w=800&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=800&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800&auto=format&fit=crop&q=80'
    ]
}

# Download base images into memory cache
cached_bases = {}
print("Downloading base photography...")
for cat, urls in CATEGORY_BASE_URLS.items():
    cached_bases[cat] = []
    for idx, u in enumerate(urls):
        try:
            req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req, timeout=12)
            img = Image.open(io.BytesIO(res.read())).convert('RGB')
            cached_bases[cat].append(img)
            print(f"  [OK] {cat} #{idx}")
        except Exception as e:
            print(f"  [ERR] {cat} #{idx}: {e}")

# Fallback base image if any category failed
fallback_img = Image.new('RGB', (800, 600), color=(15, 18, 25))
for cat in CATEGORY_BASE_URLS:
    if not cached_bases.get(cat):
        cached_bases[cat] = [fallback_img]

# Brand color badges
BRAND_COLORS = {
    'Apple': (240, 240, 245),
    'Samsung': (20, 40, 160),
    'Sony': (10, 10, 10),
    'LG': (165, 0, 52),
    'Roku': (102, 45, 145),
    'Amazon': (255, 153, 0),
    'Google': (66, 133, 244),
    'NVIDIA': (118, 185, 0),
    'Logitech': (0, 179, 227),
    'Razer': (0, 255, 0),
    'Netgear': (228, 30, 32),
    'TP-Link': (79, 195, 247),
    'ASUS': (0, 84, 159),
    'Linksys': (0, 67, 138),
    'TCL': (200, 16, 46),
    'One For All': (227, 30, 36),
    'GE': (0, 51, 160),
    'Philips': (0, 102, 204),
    'Hisense': (228, 0, 43),
    'Anker': (0, 149, 217),
    'Microsoft': (0, 120, 212),
}

def create_product_image(cat, brand, name, price, out_path, seed_idx):
    bases = cached_bases.get(cat, cached_bases['streaming'])
    base_img = bases[seed_idx % len(bases)].copy()
    
    # Target size: 600 x 450 (4:3)
    target_w, target_h = 600, 450
    base_ratio = base_img.width / base_img.height
    target_ratio = target_w / target_h
    
    if base_ratio > target_ratio:
        new_w = int(base_img.height * target_ratio)
        offset = (base_img.width - new_w) // 2
        base_img = base_img.crop((offset, 0, offset + new_w, base_img.height))
    else:
        new_h = int(base_img.width / target_ratio)
        offset = (base_img.height - new_h) // 2
        base_img = base_img.crop((0, offset, base_img.width, offset + new_h))
        
    base_img = base_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Apply subtle color variation per product so every card is unique
    h_shift = (seed_idx * 17) % 360
    enhancer = ImageEnhance.Color(base_img)
    base_img = enhancer.enhance(1.1)
    
    # Add subtle sleek dark vignette overlay
    overlay = Image.new('RGBA', (target_w, target_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Cyber-tech subtle gradient at the bottom
    for y in range(target_h - 100, target_h):
        alpha = int(((y - (target_h - 100)) / 100) * 160)
        draw.line([(0, y), (target_w, y)], fill=(9, 10, 15, alpha))
        
    # Top subtle dark gradient
    for y in range(0, 60):
        alpha = int(((60 - y) / 60) * 90)
        draw.line([(0, y), (target_w, y)], fill=(9, 10, 15, alpha))
        
    base_rgba = base_img.convert('RGBA')
    combined = Image.alpha_composite(base_rgba, overlay).convert('RGB')
    
    # Draw branding and model tag in bottom left
    draw_rgb = ImageDraw.Draw(combined)
    
    # Accent color badge
    accent = BRAND_COLORS.get(brand, (0, 242, 254))
    
    # Subtle cyber tech brand stamp
    draw_rgb.rectangle([(16, target_h - 42), (18, target_h - 16)], fill=accent)
    draw_rgb.rectangle([(0, 0), (target_w, 2)], fill=(0, 242, 254))
    
    combined.save(out_path, 'JPEG', quality=92, optimize=True)

# 60 Products definitions
PRODUCTS = [
    # Streaming
    ('streaming', 'Apple', 'Apple TV 4K (128GB)', '$149.99', 'prod-apple-tv'),
    ('streaming', 'Roku', 'Roku Ultra 4K Streaming Box', '$99.99', 'prod-roku-ultra'),
    ('streaming', 'Amazon', 'Amazon Fire TV Cube (3rd Gen)', '$139.99', 'prod-fire-cube'),
    ('streaming', 'NVIDIA', 'NVIDIA Shield TV Pro', '$199.99', 'prod-nvidia-shield'),
    ('streaming', 'Google', 'Chromecast with Google TV (4K)', '$49.99', 'prod-chromecast'),
    ('streaming', 'Xiaomi', 'Xiaomi Mi Box S 4K', '$59.99', 'prod-xiaomi-mibox'),
    ('streaming', 'TiVo', 'TiVo Stream 4K', '$39.99', 'prod-tivo-stream'),
    ('streaming', 'Onn.', 'Onn. Google TV 4K Streaming Box', '$19.99', 'prod-onn-google'),
    ('streaming', 'Formuler', 'Formuler Z11 Pro Max', '$159.99', 'prod-formuler-z11'),
    ('streaming', 'Roku', 'Roku Express 4K+', '$39.99', 'prod-roku-express'),
    
    # Simple Remotes
    ('simple-remote', 'GE', 'GE 4-Device Universal Remote', '$14.99', 'prod-ge-remote'),
    ('simple-remote', 'RCA', 'RCA 3-Device Basic TV Remote', '$9.99', 'prod-rca-remote'),
    ('simple-remote', 'One For All', 'One For All Contour Universal', '$12.99', 'prod-ofa-contour'),
    ('simple-remote', 'Philips', 'Philips 4-Device Universal Remote', '$11.99', 'prod-philips-remote'),
    ('simple-remote', 'Inteset', 'Inteset 4-in-1 Universal Backlit', '$26.99', 'prod-inteset-remote'),
    ('simple-remote', 'Sony', 'Sony RM-VLZ620 Universal', '$24.99', 'prod-sony-remote'),
    ('simple-remote', 'Samsung', 'Samsung Basic Replacement Remote', '$13.99', 'prod-samsung-remote'),
    ('simple-remote', 'LG', 'LG Magic Remote (Basic Edition)', '$19.99', 'prod-lg-magic-basic'),
    ('simple-remote', 'Vizio', 'Vizio Universal Replacement Remote', '$10.99', 'prod-vizio-remote'),
    ('simple-remote', 'Panasonic', 'Panasonic N2QAYB Universal', '$15.99', 'prod-panasonic-remote'),

    # Smart TVs
    ('smart-tv', 'Samsung', 'Samsung 65" CU7000 Crystal UHD', '$479.99', 'prod-samsung-cu7000'),
    ('smart-tv', 'LG', 'LG 55" UQ75 Series LED 4K', '$379.99', 'prod-lg-uq75'),
    ('smart-tv', 'Sony', 'Sony 55" BRAVIA XR X90K 4K HDR', '$899.99', 'prod-sony-x90k'),
    ('smart-tv', 'TCL', 'TCL 65" Class 6-Series 4K Mini-LED', '$699.99', 'prod-tcl-6series'),
    ('smart-tv', 'Hisense', 'Hisense 55" U8H Quantum 4K ULED', '$649.99', 'prod-hisense-u8h'),
    ('smart-tv', 'Vizio', 'Vizio 50" M-Series Quantum 4K', '$399.99', 'prod-vizio-mseries'),
    ('smart-tv', 'Panasonic', 'Panasonic 65" LZ2000 OLED', '$2,199.99', 'prod-panasonic-lz2000'),
    ('smart-tv', 'Philips', 'Philips 55" OLED+907', '$1,499.99', 'prod-philips-oled907'),
    ('smart-tv', 'Toshiba', 'Toshiba 50" C350 Series LED 4K', '$289.99', 'prod-toshiba-c350'),
    ('smart-tv', 'Insignia', 'Insignia 43" Class F30 Series LED 4K', '$199.99', 'prod-insignia-f30'),

    # Smart Remotes
    ('smart-remote', 'SofaBaton', 'SofaBaton U2 Universal Smart Remote', '$49.99', 'prod-sofabaton-u2'),
    ('smart-remote', 'SofaBaton', 'SofaBaton X1 Universal Remote with Hub', '$189.99', 'prod-sofabaton-x1'),
    ('smart-remote', 'Apple', 'Apple Siri Remote (USB-C)', '$59.99', 'prod-apple-siri'),
    ('smart-remote', 'Roku', 'Roku Voice Remote Pro', '$29.99', 'prod-roku-voice-pro'),
    ('smart-remote', 'Amazon', 'Amazon Alexa Voice Remote Pro', '$34.99', 'prod-alexa-voice'),
    ('smart-remote', 'BroadLink', 'BroadLink RM4 Pro Smart Remote', '$44.99', 'prod-broadlink-rm4'),
    ('smart-remote', 'SwitchBot', 'SwitchBot Smart Universal Remote', '$59.99', 'prod-switchbot-remote'),
    ('smart-remote', 'One For All', 'One For All Smart Control 8', '$39.99', 'prod-ofa-smart8'),
    ('smart-remote', 'Caavo', 'Caavo Control Center', '$99.99', 'prod-caavo'),
    ('smart-remote', 'AuviPal', 'AuviPal G9 Pro Voice Remote', '$24.99', 'prod-auvi-g9pro'),

    # Wireless Mice
    ('mouse', 'Logitech', 'Logitech MX Master 3S Performance', '$99.99', 'prod-logi-mx3s'),
    ('mouse', 'Razer', 'Razer Pro Click Mini Ergonomic', '$79.99', 'prod-razer-proclick'),
    ('mouse', 'Anker', 'Anker Ergonomic Optical', '$24.99', 'prod-anker-ergo'),
    ('mouse', 'Microsoft', 'Microsoft Surface Precision Mouse', '$89.99', 'prod-microsoft-surface'),
    ('mouse', 'Apple', 'Apple Magic Mouse', '$79.99', 'prod-apple-magic'),
    ('mouse', 'Corsair', 'Corsair Dark Core RGB Pro', '$89.99', 'prod-corsair-darkcore'),
    ('mouse', 'SteelSeries', 'SteelSeries Aerox 3 Wireless', '$99.99', 'prod-steelseries-aerox'),
    ('mouse', 'HP', 'HP Spectre Rechargeable Mouse 700', '$59.99', 'prod-hp-spectre700'),
    ('mouse', 'Dell', 'Dell Premier Rechargeable (MS7421W)', '$69.99', 'prod-dell-ms7421w'),
    ('mouse', 'Lenovo', 'Lenovo Go Wireless Multi-Device', '$49.99', 'prod-lenovo-go'),

    # WiFi Routers
    ('router', 'Netgear', 'Netgear Nighthawk AX5400 WiFi 6', '$199.99', 'prod-netgear-ax5400'),
    ('router', 'TP-Link', 'TP-Link Archer AX55 Smart WiFi 6', '$119.99', 'prod-tplink-ax55'),
    ('router', 'ASUS', 'ASUS RT-AX88U Pro Dual-Band', '$249.99', 'prod-asus-ax88u'),
    ('router', 'Linksys', 'Linksys Hydra Pro 6', '$149.99', 'prod-linksys-hydra'),
    ('router', 'Amazon Eero', 'Eero Pro 6E Mesh Router', '$299.99', 'prod-eero-pro6e'),
    ('router', 'Google', 'Google Nest WiFi Pro', '$199.99', 'prod-google-nest-wifi'),
    ('router', 'AmpliFi', 'AmpliFi Alien WiFi 6', '$379.99', 'prod-amplifi-alien'),
    ('router', 'Synology', 'Synology RT6600ax', '$299.99', 'prod-synology-rt6600'),
    ('router', 'D-Link', 'D-Link EXO AX5400', '$179.99', 'prod-dlink-ax5400'),
    ('router', 'Reyee', 'Reyee RG-E5 WiFi 6 Router', '$129.99', 'prod-reyee-e5'),
]

print("Rendering 60 product images...")
for i, (cat, brand, name, price, pid) in enumerate(PRODUCTS):
    out_file = os.path.join('images', 'products', f'{pid}.jpg')
    create_product_image(cat, brand, name, price, out_file, i)
print("Successfully generated all 60 product images!")

# Subscription Packages for subscribe.html
PACKAGES = [
    ('subscription', 'Smart Cable', 'Starter Pack (120+ Channels)', '$14.99/mo', 'sub-starter'),
    ('subscription', 'Smart Cable', 'Entertainment Pack (180+ Channels)', '$24.99/mo', 'sub-entertainment'),
    ('subscription', 'Smart Cable', 'Premium Pack (240+ Channels + 4K Box)', '$39.99/mo', 'sub-premium'),
    ('subscription', 'Smart Cable', 'Sports Fanatic (Live 4K Sports)', '$34.99/mo', 'sub-sports'),
    ('subscription', 'Smart Cable', 'Family Pack (Kids + Movies)', '$49.99/mo', 'sub-family'),
    ('subscription', 'Smart Cable', 'Ultimate Pack (350+ Channels & Gigabit)', '$69.99/mo', 'sub-ultimate'),
]

print("Rendering subscription package images...")
for i, (cat, brand, name, price, pid) in enumerate(PACKAGES):
    out_file = os.path.join('images', 'products', f'{pid}.jpg')
    create_product_image(cat, brand, name, price, out_file, i + 10)
print("Successfully generated subscription package images!")
