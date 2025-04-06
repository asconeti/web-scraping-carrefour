from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import os
import sys


# Afegeix el directori arrel al Python Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def get_url_categories():
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
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    resultats = {}
    domini = "https://www.carrefour.es"

    try:
        print("🌐 Accedint a https://www.carrefour.es/supermercado...")

        # Fins a 5 intents per obtenir els links
        links = []
        for intent in range(5):
            driver.get("https://www.carrefour.es/supermercado")
            time.sleep(0 + intent * 2)  # Espera progressiva
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            links = soup.select("a.nav-first-level-categories__list-element")

            if links:
                print(f"✅ Enllaços trobats en l'intent {intent+1}")
                break
            else:
                print(f"❌ No s'han trobat enllaços (intent {intent+1}), tornant a intentar...")

        if not links:
            print("⚠️ No s'han pogut obtenir els enllaços de categories després de 5 intents.")
            return {}

        for a in links:
            nom = a.get_text(strip=True)
            href = a.get("href")
            if nom.lower() not in ["mis productos", "ofertas"] and href:
                href_complet = domini + href if href.startswith("/") else href
                resultats[nom] = href_complet

        print(f"✅ Categories trobades: {len(resultats)}")

    except Exception as e:
        print(f"⚠️ Error inesperat, reiniciant en l'última pàgina ({pagina}): {e}")

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
        print("Ús: python source/functions/get_url.py\n")
        sys.exit(1)

    # Executa la funció principal
    try:
        get_url_categories()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


