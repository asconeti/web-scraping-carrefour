from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
def get_category_url(path_sortida):
    """
    Obté les URL de categories de productes des de Carrefour Supermercado,
    excloent "Mis productos" i "Ofertas", i les desa a un fitxer .txt.
    
    Requereix:
        - Selenium
        - BeautifulSoup
        - Driver de Chrome instal·lat al PATH
    
    Paràmetres:
        path_sortida (str): ruta del fitxer de sortida .txt
    """

    # Configura el navegador sense interfície gràfica
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    
    # Inicialitza el navegador
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("🌐 Navegant a Carrefour...")
        driver.get("https://www.carrefour.es/supermercado")
        time.sleep(5)  # espera perquè carregui tot

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Busquem tots els <a> de la navegació de categories
        links = soup.select("a.nav-first-level-categories__list-element")

        categories = []
        for a in links:
            nom = a.get_text(strip=True)
            href = a.get("href")
            if nom.lower() not in ["mis productos", "ofertas"]:
                categories.append(f"{nom} → {href}")

        # Guarda resultats
        with open(path_sortida, "w", encoding="utf-8") as f:
            for linia in categories:
                f.write(linia + "\n")

        print(f"✅ {len(categories)} categories desades a: {path_sortida}")
    
    except Exception as e:
        print("⚠️ Error:", e)
    
    finally:
        driver.quit()
        print("🚪 Tancant el navegador.")

# Exemple d'ús
get_category_url("web-scraping-practica1/data/categories.txt")
