import whois
import requests
from bs4 import BeautifulSoup
import os

##### Funcions #####

import os
from bs4 import BeautifulSoup

def processa_htmls(path_entrada, path_sortida):
    # Assegura que la carpeta de sortida existeixi
    os.makedirs(path_sortida, exist_ok=True)

    for fitxer in os.listdir(path_entrada):
        if fitxer.endswith(".html"):
            ruta_fitxer = os.path.join(path_entrada, fitxer)

            with open(ruta_fitxer, 'r', encoding='utf-8') as f:
                html = f.read()

            soup = BeautifulSoup(html, 'html.parser')

            # Crea la ruta de sortida amb extensió .txt
            nom_sortida = os.path.splitext(fitxer)[0] + '.txt'
            ruta_sortida = os.path.join(path_sortida, nom_sortida)

            with open(ruta_sortida, 'w', encoding='utf-8') as out:
                out.write(soup.prettify())

            print(f"✅ Guardat: {ruta_sortida}")



##########################################################################################################################

# Cridem a la funció:

entrada = "web-scraping-practica1/html_sources_categories"
sortida = "web-scraping-practica1/data_categories"
processa_htmls(entrada, sortida)

#######################################

