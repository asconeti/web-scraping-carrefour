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
    Aquesta funció recorre totes les pàgines d'una categoria de Carrefour, capturant productes,
    mostrant el número actual de producte llegit, el percentatge total del procés,
    i assegurant que el contingut es carrega correctament a cada pàgina.
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
        driver.get(url_categoria)
        time.sleep(5)

        # Obtenim el nombre total de productes de la categoria
        soup = BeautifulSoup(driver.page_source, "html.parser")
        pagination_info = soup.select_one(".pagination__results")
        if pagination_info:
            total_productes = int(pagination_info.find_all("span")[2].get_text(strip=True).replace("productos", "").strip())
            print(f"📊 Total productes a capturar: {total_productes}")
        else:
            total_productes = 0
            print("⚠️ No s'ha pogut trobar el nombre total de productes.")

        while True:
            print(f"📄 Processant pàgina {pagina}...")

            # Espera explícita per assegurar el carregament correcte dels productes
            wait = WebDriverWait(driver, 20)
            try:
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-card-list__item")))
            except:
                print("⚠️ Alguns productes no s'han carregat completament.")

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

            # Anàlisi de la pàgina actual
            soup = BeautifulSoup(driver.page_source, "html.parser")
            contenidor = soup.select_one("#app > div > main > div.plp-food-view__main > div.plp-food-view__container > div > div.plp-food-view__list > div.plp-food-view__results-list-container > div.plp-food-view__pagination > div > div.pagination__container")
            if not contenidor:
                print("❌ Contenidor principal no trobat")
                break

            target_li = soup.select("li.product-card-list__item")
            if not target_li:
                print("❌ No s'han trobat productes a la pàgina")
                break

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

                    productes_llegits += 1
                    percentatge = (productes_llegits / total_productes) * 100
                    print(f"✅ Producte {productes_llegits}/{total_productes} ({percentatge:.2f}%) capturat.")

                except Exception as e:
                    errors += 1
                    print(f"⚠️ Error amb un producte: {e}")

            # Navegar a la pàgina següent
            next_page = soup.select_one("#app > div > main > div.plp-food-view__main > div.plp-food-view__container > div > div.plp-food-view__list > div.plp-food-view__results-list-container > div.plp-food-view__pagination > div > div.pagination__container > div > a")
            if next_page and next_page.get("href"):
                next_page_url = f"https://www.carrefour.es{next_page.get('href')}"
                print(f"➡️ Passant a la següent pàgina: {next_page_url}")
                driver.get(next_page_url)
                time.sleep(5)  # Esperem que es carregui la pàgina
                pagina += 1
            else:
                print("📌 No hi ha més pàgines. Finalitzant scraping.")
                break

    finally:
        driver.quit()

    # Guarda DataFrame
    os.makedirs("data_scraped", exist_ok=True)
    df = pd.DataFrame(productes)
    df.to_csv("data_scraped/carrefour_products.csv", index=False)

    print(f"\n✅ Scraping complet: {productes_llegits} productes capturats de {total_productes}.")
    print(f"⚠️ Errors durant el procés: {errors}")

    return df


# Exemple d'ús
url = "https://www.carrefour.es/supermercado/productos-frescos/cat20002/c"
df = scrape_categoria_carrefour(url)