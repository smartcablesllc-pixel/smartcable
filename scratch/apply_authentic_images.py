import re
import json

with open('scratch/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

# Verified authentic direct URLs
authentic_urls = {
    'prod-apple-tv': 'https://www.apple.com/v/apple-tv-4k/am/images/overview/hero/hero_tv_remote__da02803g5doy_large.png',
    'prod-roku-ultra': 'https://images.contentstack.io/v3/assets/blt50354f32a8eecd28/blt88d3bd9595114282/67609059117e7e65ca46c8a6/ultra-pdp-carousel_cnn-badge_780x600.png?branch=production',
    'prod-fire-cube': 'https://m.media-amazon.com/images/I/61LVxM1exDL._AC_SL1000_.jpg',
    'prod-chromecast': 'https://lh3.googleusercontent.com/TQ3VHKHdvlpjlbE3woohVYFJrVBUgcVrCtHJN2xVFzkXEHNbqEiy1gS7vnxgUwHnRspROwVDgNWPUEWRxfCZC4j4mDaQD7DOACLe=rw-rj-sc0xffffffff',
    'prod-ge-remote': 'https://i5.walmartimages.com/seo/GE-4-Device-Universal-TV-Remote-Control-in-Brushed-Silver-33709_691c3b95-1bb8-445c-a151-34843398781b.2fb7dc37ec8ae8de3b489c96b1ebd462.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF',
    'prod-ofa-contour': 'https://www.oneforall.com/sites/default/files/styles/product_image_detail/public/2020-01/URC1210_new_20.png',
    'prod-philips-remote': 'https://images.philips.com/is/image/philipsconsumer/574f5169eb6d47e29a7ab0bf004c02c0?$png$&wid=410&hei=410&fit=constrain',
    'prod-samsung-cu7000': 'https://images.samsung.com/is/image/samsung/p6pim/africa_en/ua65cu7000uxly/gallery/africa-en-crystal-uhd-cu7000-ua65cu7000uxly-536771211?$1164_776_PNG$',
    'prod-lg-uq75': 'https://media.us.lg.com/transform/ecomm-PDPGallery-1100x730/3686c3dd-908d-4c6c-80ca-52ad21df07ac/md08003211-DZ-01-jpg',
    'prod-tcl-6series': 'https://ca-en.tcl.com/cdn/shop/files/R635-NFL-Front_1b8fe44e-a719-43ac-9d26-1a312046ed5e.png',
    'prod-hisense-u8h': 'https://static.wixstatic.com/media/af1c57_811b70258b1541a7a0238b734827da0e~mv2.png/v1/fill/w_507,h_358,al_c,lg_1,q_85,enc_avif,quality_auto/file.png',
    'prod-vizio-mseries': 'https://www.vizio.com/content/dam/vizio/us/en/images/product/2021/tv/m-series/m50q7-j01/gallery/2022_MQ7-Series_M50Q7-J01_Front_OS.jpg/_jcr_content/renditions/cq5dam.web.640.480.png',
    'prod-toshiba-c350': 'https://kweli.shop/wp-content/uploads/2022/11/Toshiba-50-Inch-Smart-TV-50C350-4K-UHD-VIDAA-Smart-TV.png',
    'prod-insignia-f30': 'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6448/6448758_sd.jpg',
    'prod-apple-siri': 'https://www.apple.com/v/apple-tv-4k/am/images/specs/remote__firxnq7n11qy_large.jpg',
    'prod-alexa-voice': 'https://m.media-amazon.com/images/I/61xL+BfCAeL._AC_SL1500_.jpg',
    'prod-switchbot-remote': 'https://cdn.shopify.com/s/files/1/0648/2991/5367/files/10_3x_13d54c01-e1bd-4c16-ab14-188bc11f3bc8.png?v=1718091737',
    'prod-ofa-smart8': 'https://www.oneforall.com/sites/default/files/styles/header_inner_image/public/2018-10/URC-7880.png',
    'prod-logi-mx3s': 'https://m.media-amazon.com/images/I/61ni3t1ryQL._AC_SL1500_.jpg',
    'prod-razer-proclick': 'https://assets2.razerzone.com/images/pnx.assets/c9f7763cdb2c4315862d77374302ede3/razer-pro-click-mini-2021-ogimg_1200x630.png',
    'prod-apple-magic': 'https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/MXK53?wid=2000&hei=2000&fmt=jpeg&qlt=90',
    'prod-corsair-darkcore': 'https://assets.corsair.com/image/upload/c_pad,q_85,h_1100,w_1100,f_auto/products/Gaming-Mice/CH-9315411-NA/Gallery/DARK_CORE_RGB_PRO_01.webp',
    'prod-steelseries-aerox': 'https://images.ctfassets.net/hmm5mo4qf4mf/5HgkBzBn6smRlx1iRVmxgU/b73afd509ada7a986e28df9774ff608c/aerox_3_wl_black_img_buy_01.png__1920x1080_crop-fit_optimize_subsampling-2-3637.png',
    'prod-netgear-ax5400': 'https://www.staples-3p.com/s7/is/image/Staples/sp79684454_sc7?wid=700&hei=700',
    'prod-tplink-ax55': 'https://static.tp-link.com/upload/image-line/Overview_Archer_AX55_01_normal_20210816012555m.jpg',
    'prod-asus-ax88u': 'https://kmpic.asus.com/images/2022/03/28/4426e800-6016-494f-ad65-9b46eba0bae8.png',
    'prod-google-nest-wifi': 'https://lh3.googleusercontent.com/sLmxSoy5AHmguh2LHCPscuqE9299NcMkKsfN45UcsoIrrWF5Bb-wrgcYiEm2An-B9FMoWT7GL8ytmiTkkzWYkXQVRzE7v6SLtw=rw',
    'prod-amplifi-alien': 'https://help.amplifi.com/hc/article_attachments/360050810474/afi-alien-ds-thumbnail.png',
}

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# For each product in products, find its card by ID and replace its <div class="product-card__image-wrap">...</div>
for p in products:
    pid = p['id']
    name = p['name']
    
    # Locate card in content
    # Card pattern: <div class="product-card animate-on-scroll" data-category="[^"]*" id="{pid}">
    card_pattern = rf'(id="{pid}"[^>]*>.*?<div class="product-card__image-wrap">)(.*?)(</div>)'
    
    match = re.search(card_pattern, content, re.DOTALL)
    if not match:
        print(f"Could not find card with id={pid}")
        continue
        
    before_img = match.group(1)
    after_img = match.group(3)
    
    if pid in authentic_urls:
        url = authentic_urls[pid]
        new_img = f'\n              <img class="product-card__img product-img" src="{url}" alt="{name}" loading="lazy">\n            '
    else:
        # Fallback protocol per rule 5
        new_img = f'\n              <img src="" alt="{name}" class="product-card__img product-img"> <!-- TODO: Insert actual {name} image URL here -->\n            '
        
    replacement = before_img + new_img + after_img
    content = content[:match.start()] + replacement + content[match.end():]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated index.html with authentic images and strict fallback protocol comments!")
