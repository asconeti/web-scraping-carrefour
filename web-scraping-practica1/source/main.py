import requests
from bs4 import BeautifulSoup

url = 'https://www.carrefour.es/supermercado/bebidas/cat20005/c'
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Exemple: extreure noms de productes
products = soup.find_all('a', class_='product-card__title')
for product in products:
    print(product.text.strip())
