from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Create your views here.

def get_content(product):
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    
    try:
        response = session.get(f'https://www.jumia.ci/catalog/?q={product}')
        response.raise_for_status()  # Vérifie les erreurs HTTP
    except requests.RequestException as e:
        print(f"Erreur de connexion : {e}")
        return None

    return response.text

def index(request):
    product_info_list = []

    print("Requête GET reçue :", request.GET)  # Vérifier la requête GET

    if 'product' in request.GET:
        product = request.GET.get('product')
        print("Produit recherché :", product)  # Afficher le produit recherché
        html_content = get_content(product)

        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            product_items = soup.find_all('article', class_='prd _fb col c-prod')

            for item in product_items:
                name_tag = item.find('h3', class_='name')
                price_tag = item.find('div', class_='prc')
                img_tag = item.find('img', {'data-src': True})
                stars_div = item.find('div', class_='stars _s')
                rating_div = stars_div.find('div', class_='in') if stars_div else None

                if name_tag and price_tag and img_tag and rating_div:
                    name = name_tag.text.strip()
                    price = price_tag.text.strip()
                    img_url = img_tag['data-src']
                    
                    style_attribute = rating_div.get('style', '')
                    width_value = style_attribute.split(':')[1].replace('%', '').strip() if ':' in style_attribute else '0'
                    rating = f"{float(width_value) / 20:.1f}"
                    
                    product_info = {
                        'name': name,
                        'price': price,
                        'image_url': img_url,
                        'rating': rating
                    }
                    product_info_list.append(product_info)

    return render(request, 'index.html', {'product_info_list': product_info_list})
