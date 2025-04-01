
# Anem a descriure les eines i llenguatges que utilitzarem
# per a fer el web scraping
'''
Avaluació inicial
Independentment del llenguatge utilitzat, qualsevol tipus de web scraping ha
d'incorporar una fase prèvia centrada en l'avaluació dels següents aspectes:
Bibliografia recomanada
D.￿Kouzis-Loukas (2016). Learning
Scrapy. Packt Publishing.
1) l'arxiu robots.txt,
2) el mapa del lloc web,
3) la seva grandària,
4) la tecnologia emprada i
5) el propietari del lloc web.
---------------------------------------------------------------------------------------
url: https://www.carrefour.es/
https://www.carrefour.es/robots.txt




------------------------------------
'''
import requests
import builtwith
import urllib.request

# Simula un navegador


import builtwith

url = 'https://www.carrefour.es'
info = builtwith.builtwith(url)

print("Tecnologies utilitzades per", url)
for tecnologia, detalls in info.items():
    print(f"{tecnologia}: {detalls}")
