from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os
import pandas as pd


def inicialitzar_driver():
    """
    Inicialitza un nou driver de Selenium amb configuració predefinida.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def capta_url_seguent_pagina(soup) -> str:
    """
    Captura la URL de la següent pàgina a partir del BeautifulSoup de la pàgina actual.
    Retorna la URL de la següent pàgina o None si no hi ha més pàgines.
    """
    next_page = soup.select_one("#app > div > main > div.plp-food-view__main > div.plp-food-view__container > div > div.plp-food-view__list > div.plp-food-view__results-list-container > div.plp-food-view__pagination > div > div.pagination__container > div > a")
    if next_page and next_page.get("href"):
        next_page_url = f"https://www.carrefour.es{next_page.get('href')}"
        print(f"➡️ Capturada la URL de la següent pàgina: {next_page_url}")
        return next_page_url
    else:
        print("📌 No hi ha més pàgines disponibles.")
        return None


def scrape_categoria_carrefour(driver, pagina) -> list:
    """
    Escrapeja productes de la pàgina actual utilitzant el driver Selenium.
    Retorna una llista de productes capturats.
    """
    productes = []
    soup = BeautifulSoup(driver.page_source, "html.parser")
    guardar_html_debug(soup, pagina)  # Guarda l'HTML complet per debugging

    target_li = soup.select("li.product-card-list__item")

    if not target_li:
        print("❌ No s'han trobat productes a la pàgina.")
        return productes

    for li in target_li:
        try:
            # Extracció de dades del producte
            titol_tag = li.select_one(".product-card__title-link")
            if not titol_tag:
                print("⚠️ Producte sense informació útil. Saltant...")
                continue

            descripcio = titol_tag.get_text(strip=True) if titol_tag else ""
            preu_tag = li.select_one(".product-card__price")
            preu_unitari = preu_tag.get_text(strip=True) if preu_tag else ""
            preu_kg_tag = li.select_one(".product-card__price-per-unit")
            preu_kg = preu_kg_tag.get_text(strip=True) if preu_kg_tag else ""

            media_link_tag = li.select_one(".product-card__media-link")
            url_producte = f"https://www.carrefour.es{media_link_tag.get('href')}" if media_link_tag else ""

            img_tag = li.select_one("img")
            url_imatge = img_tag.get("src") if img_tag else ""

            productes.append({
                "Descripció": descripcio,
                "Preu unitari": preu_unitari,
                "Preu/kg": preu_kg,
                "URL": url_producte,
                "Imatge": url_imatge
            })

            print(f"✅ Producte capturat: {descripcio}")

        except Exception as e:
            print(f"⚠️ Error amb un producte: {e}")

    return productes


def guardar_html_debug(soup, pagina):
    """
    Guarda l'HTML complet de la pàgina actual a un fitxer per a debugging.
    """
    os.makedirs("debug_html", exist_ok=True)  # Crea la carpeta si no existeix
    fitxer_path = f"debug_html/pagina_{pagina}.html"
    with open(fitxer_path, "w", encoding="utf-8") as fitxer:
        fitxer.write(soup.prettify())
    print(f"📝 HTML de la pàgina {pagina} guardat a {fitxer_path}")


# Inicia el bucle iteratiu extern
url = "https://www.carrefour.es/supermercado/productos-frescos/cat20002/c"
productes_totals = []
pagina = 1  # Pàgina inicial

try:
    while url:
        print(f"🔎 Processant URL: {url}")

        # Inicialitza un nou driver per cada pàgina
        driver = inicialitzar_driver()
        driver.get(url)
        time.sleep(5)  # Espera inicial abans d'interactuar amb la pàgina

        # Espera que la pàgina es carregui completament
        wait = WebDriverWait(driver, 20)
        try:
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-card-list__item")))
        except:
            print("⚠️ Alguns productes no s'han carregat completament.")

        # Pausa addicional abans de continuar
        time.sleep(5)  # Aquí afegim una espera extra per assegurar que la pàgina ha acabat de carregar

        # Scroll incremental per carregar tot el contingut dinàmic
        print("📜 Realitzant scroll incremental...")
        step = 500
        scroll_position = 0
        max_height = driver.execute_script("return document.body.scrollHeight")
        while scroll_position < max_height:
            driver.execute_script(f"window.scrollTo(0, {scroll_position});")
            time.sleep(2)
            scroll_position += step
            max_height = driver.execute_script("return document.body.scrollHeight")
        print("📜 Scroll completat!")

        # Escrapejar productes de la pàgina actual
        productes = scrape_categoria_carrefour(driver, pagina)
        productes_totals.extend(productes)

        # Obtenir la URL de la següent pàgina
        soup = BeautifulSoup(driver.page_source, "html.parser")
        time.sleep(3)  # Una altra petita pausa per assegurar que el DOM és estable
        url = capta_url_seguent_pagina(soup)
        pagina += 1  # Incrementem el número de pàgina

        # Tanca el driver abans de continuar
        driver.quit()
        print("🌐 Connexió amb el servidor interrompuda per evitar detecció.")

finally:
    print("✅ Finalització de l'scraping.")
    # Assegurem que el driver es tanca si hi ha errors
    try:
        driver.quit()
    except:
        pass

# Guarda DataFrame
os.makedirs("data_scraped", exist_ok=True)
df = pd.DataFrame(productes_totals)
df.to_csv("data_scraped/carrefour_products.csv", index=False)

print(f"\n✅ Scraping complet: {len(productes_totals)} productes capturats.")