import pykka
import requests
from bs4 import BeautifulSoup
import re

# Clase que hereda de pykka.ThreadingActor, lo que significa que cada actor se ejecuta en su propio hilo.
class SearchActor(pykka.ThreadingActor):
    # Constructor del actor de búsqueda, recibe el nombre del producto, la URL y el método de parsing.
    def __init__(self, product_name, url, parse_method):
        super().__init__()  # Llama al constructor de la clase base (pykka.ThreadingActor).
        self.product_name = product_name  # Nombre del producto a buscar.
        self.url = url  # URL de la página donde se buscará el precio.
        self.parse_method = parse_method  # Método de parsing específico para extraer el precio.

    # Método que se ejecuta cuando el actor recibe un mensaje.
    def on_receive(self, message):
        try:
            # Hace una petición GET a la URL.
            response = requests.get(self.url)
            response.raise_for_status()  # Lanza una excepción si la respuesta contiene un error HTTP.

            # Utiliza el método de parsing específico para extraer el precio del HTML recibido.
            price = self.parse_method(response.text)
            
            # Retorna un diccionario con el nombre del producto, la URL de la fuente y el precio extraído.
            return {'product': self.product_name, 'source': self.url, 'price': price}
        except requests.RequestException as e:
            # Si ocurre un error durante la solicitud, retorna un diccionario con el error.
            return {'error': str(e)}

# Método de parsing específico para extraer el precio de la página de Fullh4rd.
def parse_fullh4rd(html):
    # Convierte el contenido HTML en un objeto BeautifulSoup para facilitar la búsqueda de elementos.
    soup = BeautifulSoup(html, 'html.parser')
    
    # Busca la etiqueta <span> con la clase 'bold', que contiene el precio.
    price_text = soup.find('span', class_='bold').text
    
    # Limpia el texto del precio y lo convierte a un número con la función 'clean_price'.
    price = clean_price(price_text)
    return price  # Retorna el precio limpio y convertido a número.

# Método de parsing para extraer el precio de una página de MercadoLibre.
def parse_mercadolibre(html):
    # Convierte el contenido HTML en un objeto BeautifulSoup.
    soup = BeautifulSoup(html, 'html.parser')
    
    # Busca la etiqueta <meta> con el atributo 'itemprop'='price', que contiene el precio en el valor 'content'.
    meta_tag = soup.find('meta', {'itemprop': 'price'})
    
    # Convierte el contenido del meta tag a un número flotante, ya que MercadoLibre almacena el precio en formato numérico.
    price = float(meta_tag['content'])
    return price  # Retorna el precio.

# Método de parsing para extraer el precio de una página de Shoppingnet.
def parse_shoppingnet(html):
    # Convierte el contenido HTML en un objeto BeautifulSoup.
    soup = BeautifulSoup(html, 'html.parser')
    
    # Busca la etiqueta <span> con la clase 'andes-money-amount__fraction', que contiene el precio.
    price_text = soup.find('span', class_='andes-money-amount__fraction', attrs={'aria-hidden': 'true'}).text
    
    # Limpia el texto del precio y lo convierte a número usando la función 'clean_price'.
    price = clean_price(price_text)
    return price  # Retorna el precio limpio y convertido a número.

# Método de parsing para extraer el precio de una página de 4KRC.
def parse_4krc(html):
    # Convierte el contenido HTML en un objeto BeautifulSoup.
    soup = BeautifulSoup(html, 'html.parser')
    
    # Busca la etiqueta <span> con la clase 'andes-money-amount__fraction', que contiene el precio.
    price_text = soup.find('span', class_='andes-money-amount__fraction', attrs={'aria-hidden': 'true'}).text
    
    # Limpia el texto del precio y lo convierte a número usando la función 'clean_price'.
    price = clean_price(price_text)
    return price  # Retorna el precio limpio y convertido a número.

# Método de parsing para extraer el precio de una página de GamingCity.
def parse_gamingcity(html):
    # Convierte el contenido HTML en un objeto BeautifulSoup.
    soup = BeautifulSoup(html, 'html.parser')
    
    # Busca la etiqueta <span> con la clase 'andes-money-amount__fraction', que contiene el precio.
    price_text = soup.find('span', class_='andes-money-amount__fraction', attrs={'aria-hidden': 'true'}).text
    
    # Limpia el texto del precio y lo convierte a número usando la función 'clean_price'.
    price = clean_price(price_text)
    return price  # Retorna el precio limpio y convertido a número.

# Función auxiliar para limpiar el texto del precio y convertirlo a un número flotante.
def clean_price(price_text):
    # Elimina cualquier carácter que no sea un dígito o coma (por ejemplo, signos de moneda).
    # Luego, reemplaza la coma por un punto para que Python pueda interpretarlo como un número flotante.
    cleaned_price = re.sub(r'[^\d,]', '', price_text).replace(',', '.')
    
    # Convierte el precio limpio a un número flotante y lo retorna.
    return float(cleaned_price)
