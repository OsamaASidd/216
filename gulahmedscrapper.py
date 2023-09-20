import requests
from bs4 import BeautifulSoup
import json
headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}
req = requests.get('https://www.gulahmedshop.com/women/ideas-pret/stitched-suits',headers=headers)
soup = BeautifulSoup(req.content, 'html.parser')
product_items = soup.find_all('div', class_='product details product-item-details')
product_list = []

for item in product_items:
    product_id = item.find('div', {'data-product-id': True})
    product_name = item.find("strong", class_="product name product-item-name")
    
    old_price_span = item.find('span', {'class': 'price-wrapper', 'data-price-type': 'oldPrice'})
    if old_price_span:
        old_price_text = old_price_span.find('span', {'class': 'price'}).get_text(strip=True).split()[-1]
        old_price = float(old_price_text.replace(',', ''))
    else:
        old_price_text = None
        
        
    current_price_span = item.find('span', {'class': 'price-wrapper', 'data-price-type': 'finalPrice'})
    if current_price_span:
        current_price_text = current_price_span.find('span', {'class': 'price'}).get_text(strip=True).split()[-1]
        current_price = float(current_price_text.replace(',', ''))
    else:
        current_price = None    
    
    
    product_url_tag = item.find('a', href=True)
    if product_url_tag:
        product_url = product_url_tag['href']
    else:
        product_url = None    
        
        
    img_tag = item.find('img')
    if img_tag:
        product_image_url = img_tag['data-desk-owlsrc']
    else:
        product_image_url = None
        
    
    
    discount_percentage = round(((old_price - current_price) / old_price) * 100)
        
    product_details = {
            "brand": "GulAhmed",
            "productID": product_id['data-product-id'],
            "name": product_name.text.strip(),
            "oldPrice": old_price,
            "currentPrice": current_price,
            "Discount": discount_percentage,
            "url" : product_url,
            "Image-url" :  product_image_url
        }
        
       
    product_list.append(product_details)
    
product_json = json.dumps(product_list, indent=4)

print(product_json)
