import re

verified_images = {
    'prod-nvidia-shield': 'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6370/6370425_sd.jpg',
    'prod-xiaomi-mibox': 'https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E875F0267/pms_1681282654.56587528.png',
    'prod-tivo-stream': 'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6470/6470822_sd.jpg',
    'prod-onn-google': 'https://i5.walmartimages.com/seo/onn-Google-TV-4K-Streaming-Box-New-2023-4K-UHD-Resolution_b88ec6f0-e014-4071-a66c-6d6050079e72.b04e9223fea65d1167ff334cc467847a.png?odnHeight=768&odnWidth=768&odnBg=FFFFFF',
    'prod-formuler-z11': 'https://static.wixstatic.com/media/82c044_bc2cf429001e405b9545fcbe23c8a150~mv2.jpg',
    'prod-roku-express': 'https://i5.walmartimages.com/seo/Roku-Express-4K-Streaming-Player-HD-4K-HDR-with-Roku-Voice-Remote-with-TV-Controls_7eb811ad-e3ad-48d0-8179-253553bc6cd2.57215fc97b572ca619839e9017ae0ec7.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF',
    'prod-rca-remote': 'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6537/6537924_sd.jpg',
    'prod-inteset-remote': 'https://m.media-amazon.com/images/I/41lbxJUJWjL.jpg',
    'prod-sony-remote': 'https://m.media-amazon.com/images/I/817lPc1KHoL._AC_SL1500_.jpg',
    'prod-samsung-remote': 'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6401/6401035_sd.jpg',
    'prod-lg-magic-basic': 'https://m.media-amazon.com/images/I/71ZX6IUxHkL._SL1500_.jpg',
    'prod-vizio-remote': 'https://m.media-amazon.com/images/I/41JCQjrf5fL.jpg',
    'prod-panasonic-remote': 'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/1272/12720143_sd.jpg',
    'prod-sony-x90k': 'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6499/6499804_sd.jpg',
    'prod-panasonic-lz2000': 'https://sk.panasonic.com/wp-content/uploads/2022/10/TX-65LZ2000E_001.jpg',
    'prod-philips-oled907': 'https://images.philips.com/is/image/PhilipsConsumer/55OLED907_12-IMS-en_US?wid=800',
    'prod-sofabaton-u2': 'images/products/prod-sofabaton-u2.png',
    'prod-sofabaton-x1': 'https://www.sofabaton.com/wp-content/uploads/2023/10/sofabaton-x1-universal-remote-control.png',
    'prod-roku-voice-pro': 'https://i5.walmartimages.com/seo/Roku-Voice-Remote-Pro-2nd-Ed-Rechargeable-TV-Remote-Control-Hands-free-Voice-Controls-Backlit-Buttons-Lost-Remote-Finder-Replacement-Remote-Compatibl_9776b215-7136-477f-84ad-c03cbb06a897.d761f877965a426f16ecdfb80febe716.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF',
    'prod-broadlink-rm4': 'https://m.media-amazon.com/images/I/51t7+8NmPXL.jpg',
    'prod-caavo': 'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6302/6302877_sd.jpg',
    'prod-auvi-g9pro': 'https://m.media-amazon.com/images/S/aplus-media/sc/fd2ff7ad-0914-410b-8dea-7d98dea80a4d.__CR0,0,300,400_PT0_SX300_V1___.jpg',
    'prod-anker-ergo': 'https://i5.walmartimages.com/seo/Anker-Ergonomic-Optical-USB-Wired-Vertical-Mouse-1000-1600-DPI-5-Buttons-CE100_f2b61ebd-bcec-4221-be27-e8b3924223cb.ea435d7f385ebeb358baf83b3f18c699.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF',
    'prod-microsoft-surface': 'https://i5.walmartimages.com/seo/Microsoft-Surface-Precision-Mouse-Bluetooth-4-0-Gray_bca159f7-cb2b-497a-820d-a0740895ca66.997e325539a4bc1c4a570047aff8271b.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF',
    'prod-hp-spectre700': 'https://m.media-amazon.com/images/I/71XwLX0ySeL.jpg',
    'prod-dell-ms7421w': 'https://i.dell.com/is/image/DellContent//content/dam/ss2/product-images/peripherals/input-devices/dell/mouse/ms7421w/general/ms7421w_pkg_01.jpg?fmt=jpg&wid=800&hei=600',
    'prod-lenovo-go': 'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/1123/11235092_sd.jpg',
    'prod-linksys-hydra': 'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6494/6494020_sd.jpg',
    'prod-eero-pro6e': 'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6495/6495915_sd.jpg',
    'prod-synology-rt6600': 'https://www.synology.com/img/products/detail/RT6600ax/img_og_image.jpg',
    'prod-dlink-ax5400': 'https://aphnetworks.com/article_images/reviews/d-link-dir-x5460/004.jpg',
    'prod-reyee-e5': 'https://eo-sgp-cos.ruijie.com/FU/Upload/Product/2022/6-15/202261539583467.jpg'
}

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

updated = 0
for pid, url in verified_images.items():
    # Match card block and replace img src regardless of attribute order
    pattern = r'(id="' + re.escape(pid) + r'"[^>]*>.*?<img[^>]*?\ssrc=")([^"]*)(")'
    def repl(m):
        global updated
        updated += 1
        return m.group(1) + url + m.group(3)
    
    html, count = re.subn(pattern, repl, html, count=1, flags=re.DOTALL)
    if count == 0:
        print(f"Warning: pattern did not match for {pid}")

# Clean up TODO comments
html = re.sub(r'\s*<!--\s*TODO:\s*Insert actual[^>]*?-->', '', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Successfully updated {updated} / {len(verified_images)} images in index.html!")
