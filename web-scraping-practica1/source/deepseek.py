from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import os
import pandas as pd
import requests
import random

def scrape_categoria_carrefour(url_categoria: str) -> pd.DataFrame:
    """
    Funció millorada per scraping a Carrefour amb protecció contra Cloudflare.
    Inclou comportament humà, gestió de cookies i tècniques anti-detecció.
    """
    # Configuració avançada del navegador
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    options.add_argument("--window-size=1920,1080")

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    
    # Ocultar automatització
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        window.navigator.chrome = {
            runtime: {},
        };
        '''
    })

    print(f"🔎 Iniciant scraping a: {url_categoria}")

    productes = []
    errors = 0
    productes_llegits = 0
    pagina = 1
    max_pagines = 10  # Límit de seguretat

    try:
        # Visita inicial per establir sessió
        driver.get("https://www.carrefour.es")
        time.sleep(random.uniform(3, 6))
        
        while pagina <= max_pagines:
            url_pagina = f"{url_categoria}?page={pagina}" if pagina > 1 else url_categoria
            print(f"➡️ Processant pàgina {pagina}: {url_pagina}")
            
            driver.get(url_pagina)
            time.sleep(random.uniform(4, 8))  # Espera aleatòria
            
            # Scroll natural amb comportament humà
            print("📜 Realitzant scroll natural...")
            for _ in range(3):
                scroll_amount = random.randint(300, 800)
                driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                time.sleep(random.uniform(0.5, 2.5))
            
            # Espera explícita pels productes
            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-card-list__item"))
                )
            except Exception as e:
                print(f"⚠️ Error esperant productes: {e}")
                break

            # Processar productes amb BeautifulSoup
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
                    titol_tag = li.select_one(".product-card__title-link")
                    if not titol_tag:
                        continue

                    # Extreure dades del producte
                    descripcio = titol_tag.get_text(strip=True)
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
                    print(f"✅ Producte {productes_llegits} capturat")

                except Exception as e:
                    errors += 1
                    print(f"⚠️ Error amb un producte: {e}")

            # Paginació amb comportament humà
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-label='Página siguiente']"))
                )
                
                # Simular comportament humà
                ActionChains(driver).move_to_element(next_button).pause(1).perform()
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", next_button)
                time.sleep(random.uniform(1, 3))
                
                # Clic amb JavaScript
                driver.execute_script("arguments[0].click();", next_button)
                
                # Espera després del canvi de pàgina
                time.sleep(random.uniform(4, 7))
                pagina += 1
                
            except Exception as e:
                print(f"❌ Fi de les pàgines o error de paginació: {e}")
                break

    finally:
        driver.quit()

    # Guardar resultats
    df = pd.DataFrame(productes)
    os.makedirs("data_scraped", exist_ok=True)
    df.to_csv("data_scraped/carrefour_products.csv", index=False)

    print(f"\n✅ Scraping completat: {len(productes)} productes capturats")
    print(f"⚠️ Errors durant el procés: {errors}")

    return df


# Exemple d'ús
if __name__ == "__main__":
    url = "https://www.carrefour.es/supermercado/productos-frescos/cat20002/c"
    df = scrape_categoria_carrefour(url)
    print(df.head())
    