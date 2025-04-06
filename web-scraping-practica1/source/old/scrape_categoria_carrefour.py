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
import requests


def scrape_categoria_carrefour(url_categoria: str) -> pd.DataFrame:
    """
    Aquesta funció navega dins una categoria de Carrefour, assegura que tot el contingut es carrega amb scroll repetitiu,
    espera explícita, i afegeix el link de la web del producte al DataFrame final.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    print(f"🔎 Iniciant scraping a: {url_categoria}")

    productes = []
    errors = 0
    productes_llegits = 0
    pagina = 1

    try:
        while True:
            url_pagina = url_categoria if pagina == 1 else f"{url_categoria}?offset={(pagina - 1) * 24}"
            driver.get(url_pagina)
            time.sleep(3)

            # Espera explícita per assegurar el carregament dels productes
            wait = WebDriverWait(driver, 20)
            try:
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-card-list__item")))
            except:
                print("⚠️ Alguns productes no s'han carregat completament.")

            # Scroll incremental per carregar contingut dinàmic
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

            soup = BeautifulSoup(driver.page_source, "html.parser")
            contenidor = soup.select_one("#app > div > main > div.plp-food-view__main > div.plp-food-view__container")
            if not contenidor:
                print("❌ Contenidor principal no trobat")
                break

            target_li = contenidor.select("li.product-card-list__item")
            if not target_li:
                print("❌ No s'han trobat productes a la pàgina")
                break

            for li in target_li:
                try:
                    print("🖨️ Debugging HTML del producte:")
                    print(li.prettify())  # Imprimeix l'estructura HTML completa del producte

                    # Comprovar si l'element conté informació mínima
                    titol_tag = li.select_one(".product-card__title-link")
                    if not titol_tag:
                        print("⚠️ Producte sense informació útil. Saltant...")
                        continue

                    parent = li.select_one(".product-card__parent") or li.select_one(".product-card-list__lazy-card")
                    cataleg = parent.get("catalog", "") if parent else "Desconegut"

                    # Verifica si el producte és patrocinat
                    patrocinat_tag = li.select_one(".product-card__sponsored-text")
                    patrocinat = patrocinat_tag.get_text(strip=True) if patrocinat_tag else "No patrocinado"

                    descripcio = titol_tag.get_text(strip=True) if titol_tag else ""

                    preu_tag = li.select_one(".product-card__price")
                    preu_unitari = preu_tag.get_text(strip=True) if preu_tag else ""

                    preu_kg_tag = li.select_one(".product-card__price-per-unit")
                    preu_kg = preu_kg_tag.get_text(strip=True) if preu_kg_tag else ""

                    # URL del producte (link de la web)
                    media_link_tag = li.select_one(".product-card__media-link")
                    url_producte = f"https://www.carrefour.es{media_link_tag.get('href')}" if media_link_tag else ""

                    # Imatge
                    img_tag = li.select_one("img")
                    url_imatge = img_tag.get("src") if img_tag else ""
                    nom_imatge = url_imatge.split("/")[-1] if url_imatge else ""

                    if url_imatge:
                        os.makedirs("data_scraped/media", exist_ok=True)
                        imatge_path = f"data_scraped/media/{nom_imatge}"
                        try:
                            img_data = requests.get(url_imatge).content
                            with open(imatge_path, "wb") as handler:
                                handler.write(img_data)
                        except:
                            pass

                    productes.append({
                        "Cataleg": cataleg,
                        "Patrocinat": patrocinat,
                        "Descripció": descripcio,
                        "Preu unitari": preu_unitari,
                        "Preu/kg": preu_kg,
                        "URL": url_producte,  # Afegit al DataFrame
                        "Imatge": url_imatge
                    })
                    productes_llegits += 1
                    print(f"✅ Producte {productes_llegits} capturat")

                except Exception as e:
                    errors += 1
                    print(f"⚠️ Error amb un producte: {e}")

            # Paginació
            pagination = soup.select_one(".pagination")
            if pagination and f"offset={pagina * 24}" in str(pagination):
                pagina += 1
            else:
                break

    finally:
        driver.quit()

    # Guarda DataFrame
    df = pd.DataFrame(productes)
    os.makedirs("data_scraped", exist_ok=True)
    df.to_csv("data_scraped/carrefour_products.csv", index=False)

    print(f"\n✅ Total productes capturats: {len(productes)}")
    print(f"⚠️ Total productes amb error: {errors}")

    return df


# Exemple d'ús
url = "https://www.carrefour.es/supermercado/productos-frescos/cat20002/c"
df = scrape_categoria_carrefour(url)