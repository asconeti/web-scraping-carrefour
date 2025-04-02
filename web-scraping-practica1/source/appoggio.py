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


#####FUNCIO###########################


def extreu_filtres_de_categories(carpeta_entrada, carpeta_sortida):
    """
    Itera per tots els fitxers .txt d'una carpeta, analitza el seu contingut HTML i extreu els filtres
    en format "etiqueta → URL", desant els resultats en fitxers .txt dins una altra carpeta.

    Paràmetres:
        carpeta_entrada (str): Ruta amb fitxers .txt (HTML formatat).
        carpeta_sortida (str): Ruta on es desaran els resultats.
    """
    os.makedirs(carpeta_sortida, exist_ok=True)

    for fitxer in os.listdir(carpeta_entrada):
        if fitxer.endswith('.txt'):
            ruta_entrada = os.path.join(carpeta_entrada, fitxer)
            nom_sortida = os.path.splitext(fitxer)[0] + '_filtres.txt'
            ruta_sortida = os.path.join(carpeta_sortida, nom_sortida)

            with open(ruta_entrada, 'r', encoding='utf-8') as f:
                html = f.read()

            soup = BeautifulSoup(html, 'html.parser')
            filtres = soup.find_all("li", class_="facet__list__item")

            with open(ruta_sortida, 'w', encoding='utf-8') as out:
                for filtre in filtres:
                    etiqueta = filtre.get_text(strip=True)
                    enllac = filtre.find("a")
                    url = enllac["href"] if enllac and "href" in enllac.attrs else "—"
                    out.write(f"{etiqueta} → {url}\n")

            print(f"✅ Filtres extrets de: {fitxer} → Guardat a: {ruta_sortida}")

#############################################

# Cridem a les funcións:

entrada = "web-scraping-practica1/html_sources_categories"
sortida = "web-scraping-practica1/data_categories"
processa_htmls(entrada, sortida)

extreu_filtres_de_categories(
    carpeta_entrada="web-scraping-practica1/data_categories",
    carpeta_sortida="web-scraping-practica1/categories_filtrades"
)
