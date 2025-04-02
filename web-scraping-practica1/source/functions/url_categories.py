from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import os
import sys

# Afegeix el directori arrel al Python Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def get_category_url():
    """
    Accedeix a la pàgina de Carrefour Supermercado, extreu les categories de productes
    (excloent "Mis productos" i "Ofertas") i retorna un diccionari amb el format:
    {"Nom de categoria": "URL completa"}
    
    Retorna:
        dict: Diccionari amb les categories i les seves URL absolutes.
    """

    # ⚙️ Configura opcions del navegador
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # utilitzem un user-agent per evitar bloquejos
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/122.0.0.0 Safari/537.36")

    # Indica a Selenium on està ubicat el binari del chromedriver dins del sistema operatiu
    #  (en aquest cas dins del contenidor Linux).
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    # Diccionari per emmagatzemar categories i URLs
    resultats = {}
    domini = "https://www.carrefour.es"

    try:
        print("🌐 Accedint a Carrefour...")
        # Petició a la pàgina de Carrefour Supermercado. Carreguem completament la pàgina
        # damunt de l'objecte driver.
        driver.get("https://www.carrefour.es/supermercado")
        time.sleep(5)  # espera que carregui

        # Obtenim el contingut HTML complet de la pàgina
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # Selecciona els enllaços de categoria, aquest selector CSS selecciona
        # tots els elements <a> que tenen la classe CSS "nav-first-level-categories__list-element".
        links = soup.select("a.nav-first-level-categories__list-element")

        # Desa les categories i URLs en un diccionari
        for a in links:
            nom = a.get_text(strip=True)
            href = a.get("href")
            if nom.lower() not in ["mis productos", "ofertas"] and href:
                href_complet = domini + href if href.startswith("/") else href
                resultats[nom] = href_complet

        print(f"✅ Categories trobades: {len(resultats)}")

    except Exception as e:
        print("⚠️ Error:", e)

    finally:
        driver.quit()

    return resultats

##################################

# Aquest bloc s'executa només quan el fitxer on està definit és
# executat directament com a script principal. Això vol dir que
# si la funció get_category_url() és importada (bé cridada) desde
# un altre script, per exemple des de "main.py", aquest bloc no s'executarà.
# Si jo l'executo directament des del terminal Python a través de la línia d'ordres',
# aquest bloc si s'executarà.
if __name__ == "__main__":
    # Comprova que s'ha passat el nombre correcte d'arguments
    if len(sys.argv) != 1:
        print("Ús: python source/functions/url_categories.py\n")
        sys.exit(1)

    # Executa la funció principal
    try:
        get_category_url()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


