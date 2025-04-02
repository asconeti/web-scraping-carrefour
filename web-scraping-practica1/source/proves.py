from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import os

def get_category_url(path_sortida):
    """
    Obté les URL de categories de productes des de Carrefour Supermercado,
    excloent "Mis productos" i "Ofertas", i les desa en un fitxer .txt
    i en un diccionari Python (retornat per la funció).

    Args:
        path_sortida (str): Ruta del fitxer de sortida .txt

    Returns:
        dict: Diccionari amb {categoria: url}
    """

    # 🔧 Configura Chrome amb user-agent i opcions per entorns headless
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )

    # 🚀 Llança el navegador indicant el path del chromedriver
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    resultats = {}  # Diccionari per desar categories i URLs

    try:
        print("🌐 Navegant a https://www.carrefour.es/supermercado...")
        driver.get("https://www.carrefour.es/supermercado")
        time.sleep(5)

        # 🔍 Obté el contingut HTML complet
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # 📌 Selecciona els enllaços de categoria
        # Aquesta línia fa servir BeautifulSoup per trobar tots els elements <a>
        # (enllaços) de l’HTML que tenen la classe CSS nav-first-level-categories__list-element.
        links = soup.select("a.nav-first-level-categories__list-element")

        # 📂 Desa les categories i URLs en un diccionari
        with open(path_sortida, "w", encoding="utf-8") as f:
            for a in links:
                nom = a.get_text(strip=True)
                href = a.get("href")
                if nom.lower() not in ["mis productos", "ofertas"] and href:
                    resultats[nom] = href
                    f.write(f"{nom} → {href}\n")

        print(f"✅ {len(resultats)} categories desades a: {path_sortida}")

    except Exception as e:
        print("⚠️ Error:", e)

    finally:
        driver.quit()

    return resultats


########Exemple d'ús

diccionari_categories = get_category_url("web-scraping-practica1/url_categories/categories.txt")

# Veure el resultat per consola
for categoria, url in diccionari_categories.items():
    print(f"{categoria} : {url}")

print(diccionari_categories)

