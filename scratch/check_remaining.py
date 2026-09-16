verified = {
    'prod-nvidia-shield': 'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6370/6370425_sd.jpg',
    'prod-onn-google': 'https://i5.walmartimages.com/seo/onn-Google-TV-4K-Streaming-Box-New-2023-4K-UHD-Resolution_b88ec6f0-e014-4071-a66c-6d6050079e72.b04e9223fea65d1167ff334cc467847a.png?odnHeight=768&odnWidth=768&odnBg=FFFFFF',
    'prod-roku-express': 'https://i5.walmartimages.com/seo/Roku-Express-4K-Streaming-Player-HD-4K-HDR-with-Roku-Voice-Remote-with-TV-Controls_7eb811ad-e3ad-48d0-8179-253553bc6cd2.57215fc97b572ca619839e9017ae0ec7.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF',
    'prod-roku-voice-pro': 'https://i5.walmartimages.com/seo/Roku-Voice-Remote-Pro-2nd-Ed-Rechargeable-TV-Remote-Control-Hands-free-Voice-Controls-Backlit-Buttons-Lost-Remote-Finder-Replacement-Remote-Compatibl_9776b215-7136-477f-84ad-c03cbb06a897.d761f877965a426f16ecdfb80febe716.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF',
    'prod-anker-ergo': 'https://i5.walmartimages.com/seo/Anker-Ergonomic-Optical-USB-Wired-Vertical-Mouse-1000-1600-DPI-5-Buttons-CE100_f2b61ebd-bcec-4221-be27-e8b3924223cb.ea435d7f385ebeb358baf83b3f18c699.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF',
    'prod-microsoft-surface': 'https://i5.walmartimages.com/seo/Microsoft-Surface-Precision-Mouse-Bluetooth-4-0-Gray_bca159f7-cb2b-497a-820d-a0740895ca66.997e325539a4bc1c4a570047aff8271b.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF',
    'prod-tivo-stream': 'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6470/6470822_sd.jpg',
    'prod-sony-x90k': 'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6499/6499804_sd.jpg',
    'prod-linksys-hydra': 'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6494/6494020_sd.jpg',
    'prod-dell-ms7421w': 'https://i.dell.com/is/image/DellContent//content/dam/ss2/product-images/peripherals/input-devices/dell/mouse/ms7421w/general/ms7421w_pkg_01.jpg?fmt=jpg&wid=800&hei=600',
    'prod-sofabaton-u2': 'images/products/prod-sofabaton-u2.png',
    'prod-sony-remote': 'https://m.media-amazon.com/images/I/817lPc1KHoL._AC_SL1500_.jpg',
    'prod-panasonic-lz2000': 'https://sk.panasonic.com/wp-content/uploads/2022/10/TX-65LZ2000E_001.jpg',
    'prod-inteset-remote': 'https://m.media-amazon.com/images/I/41lbxJUJWjL.jpg',
    'prod-lg-magic-basic': 'https://m.media-amazon.com/images/I/71ZX6IUxHkL._SL1500_.jpg',
    'prod-vizio-remote': 'https://m.media-amazon.com/images/I/41JCQjrf5fL.jpg',
    'prod-hp-spectre700': 'https://m.media-amazon.com/images/I/71XwLX0ySeL.jpg',
    'prod-philips-oled907': 'https://images.philips.com/is/image/PhilipsConsumer/55OLED907_12-IMS-en_US?wid=800',
    'prod-synology-rt6600': 'https://www.synology.com/img/products/detail/RT6600ax/img_og_image.jpg'
}

print(f"Verified count: {len(verified)} / 32")

import json
with open('scratch/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

needed_ids = [
    "prod-nvidia-shield", "prod-xiaomi-mibox", "prod-tivo-stream", "prod-onn-google",
    "prod-formuler-z11", "prod-roku-express", "prod-rca-remote", "prod-inteset-remote",
    "prod-sony-remote", "prod-samsung-remote", "prod-lg-magic-basic", "prod-vizio-remote",
    "prod-panasonic-remote", "prod-sony-x90k", "prod-panasonic-lz2000", "prod-philips-oled907",
    "prod-sofabaton-u2", "prod-sofabaton-x1", "prod-roku-voice-pro", "prod-broadlink-rm4",
    "prod-caavo", "prod-auvi-g9pro", "prod-anker-ergo", "prod-microsoft-surface",
    "prod-hp-spectre700", "prod-dell-ms7421w", "prod-lenovo-go", "prod-linksys-hydra",
    "prod-eero-pro6e", "prod-synology-rt6600", "prod-dlink-ax5400", "prod-reyee-e5"
]

remaining = [p for p in products if p['id'] in needed_ids and p['id'] not in verified]
print(f"Remaining: {len(remaining)}")
for r in remaining:
    print(f"  {r['id']:25s} | {r['brand']:15s} | {r['name']}")
