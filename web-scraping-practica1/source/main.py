import requests
from bs4 import BeautifulSoup

url = "https://www.carrefour.es/supermercado"
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')

for link in soup.find_all('a'):
    print(link.get('href'))

