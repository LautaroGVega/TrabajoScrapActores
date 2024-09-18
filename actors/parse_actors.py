import pykka
from bs4 import BeautifulSoup
import json

class ParseActor(pykka.ThreadingActor):
    def __init__(self, format_type='html'):
        super().__init__()
        self.format_type = format_type  # Tipo de formato: 'html' o 'json'

    def on_receive(self, message):
        if 'price_data' in message:
            try:
                if self.format_type == 'html':
                    return self._parse_html(message['price_data'])
                elif self.format_type == 'json':
                    return self._parse_json(message['price_data'])
            except Exception as e:
                return {'error': f"Error parsing data: {str(e)}"}
        return {'error': 'Invalid message format'}

    def _parse_html(self, html_content):
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            # Extraer el precio del HTML usando selectores CSS
            price_tag = soup.select_one('.price')  # Ejemplo: usa la clase 'price'
            if price_tag:
                price = price_tag.text.strip()
                return {'price': float(price.replace('$', '').replace(',', ''))}
            else:
                return {'error': 'Price tag not found in HTML'}
        except Exception as e:
            return {'error': f"Error parsing HTML: {str(e)}"}

    def _parse_json(self, json_content):
        try:
            data = json.loads(json_content)
            # Suponer que el precio está en una clave 'price'
            if 'price' in data:
                return {'price': data['price']}
            else:
                return {'error': 'Price not found in JSON'}
        except json.JSONDecodeError as e:
            return {'error': f"Error parsing JSON: {str(e)}"}
