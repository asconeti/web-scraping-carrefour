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
    Aquesta funció navega dins una categoria de Carrefour, recorre totes les pàgines de productes
    (evitant els productes en "carousel"), i extreu les dades desitjades de cada producte:
    - Catàleg, categoria, descripció, preu unitari, preu/kg, promocions, URL i foto del producte.

    Guarda el DataFrame final en un arxiu CSV i descarrega les imatges a /data_scraped/media.
    """

    # 🔧 Configura Selenium
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
    max_intents = 3
    pagina = 1

    try:
        while True:
            url_pagina = url_categoria if pagina == 1 else f"{url_categoria}?offset={(pagina - 1) * 24}"
            driver.get(url_pagina)
            time.sleep(5)
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
                    parent = li.select_one(".product-card__parent") or li.select_one(".product-card-list__lazy-card")
                    if not parent:
                        raise Exception("Producte sense contenidor .product-card__parent")

                    cataleg = parent.get("catalog", "")

                    titol_tag = li.select_one(".product-card__title-link")
                    descripcio = titol_tag.get_text(strip=True) if titol_tag else ""

                    preu_tag = li.select_one(".product-card__price")
                    preu_unitari = preu_tag.get_text(strip=True) if preu_tag else ""

                    preu_kg_tag = li.select_one(".product-card__price-per-unit")
                    preu_kg = preu_kg_tag.get_text(strip=True) if preu_kg_tag else ""

                    promo_tag = li.select_one(".badge__name")
                    promocio = promo_tag.get_text(strip=True) if promo_tag else ""

                    href = titol_tag.get("href") if titol_tag else ""
                    url_producte = f"https://www.carrefour.es{href}" if href else ""

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
                        "Descripció": descripcio,
                        "Preu unitari": preu_unitari,
                        "Preu/kg": preu_kg,
                        "Promoció": promocio,
                        "URL": url_producte,
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
    df.to_csv("data_scraped/mercadona_food_products.csv", index=False)

    print(f"\n✅ Total productes capturats: {len(productes)}")
    print(f"⚠️ Total productes amb error: {errors}")

    return df



url = "https://www.carrefour.es/supermercado/productos-frescos/cat20002/c"
df = scrape_categoria_carrefour(url)
