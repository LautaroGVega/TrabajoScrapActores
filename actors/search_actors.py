import pykka
import requests
from bs4 import BeautifulSoup
import re

class SearchActor(pykka.ThreadingActor):
    def __init__(self, product_name, url, parse_method):
        super().__init__()
        self.product_name = product_name
        self.url = url
        self.parse_method = parse_method

    def on_receive(self, message):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            
            price = self.parse_method(response.text)
            return {'product': self.product_name, 'source': self.url, 'price': price}
        except requests.RequestException as e:
            return {'error': str(e)}

def parse_fullh4rd(html):
    soup = BeautifulSoup(html, 'html.parser')
    price_text = soup.find('span', class_='bold').text
    price = clean_price(price_text)
    return price

def parse_mercadolibre(html):
    soup = BeautifulSoup(html, 'html.parser')
    meta_tag = soup.find('meta', {'itemprop': 'price'})
    price = float(meta_tag['content'])  # MercadoLibre ya tiene el precio en formato numérico
    return price

def parse_shoppingnet(html):
    soup = BeautifulSoup(html, 'html.parser')
    price_text = soup.find('span', class_='andes-money-amount__fraction', attrs={'aria-hidden': 'true'}).text
    price = clean_price(price_text)
    return price

def parse_4krc(html):
    soup = BeautifulSoup(html, 'html.parser')
    price_text = soup.find('span', class_='andes-money-amount__fraction', attrs={'aria-hidden': 'true'}).text
    price = clean_price(price_text)
    return price

def parse_gamingcity(html):
    soup = BeautifulSoup(html, 'html.parser')
    price_text = soup.find('span', class_='andes-money-amount__fraction', attrs={'aria-hidden': 'true'}).text
    price = clean_price(price_text)
    return price

def clean_price(price_text):
    # Eliminar cualquier carácter que no sea dígito o coma y cambiar la coma decimal a punto
    cleaned_price = re.sub(r'[^\d,]', '', price_text).replace(',', '.')
    return float(cleaned_price)
