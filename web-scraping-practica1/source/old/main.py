

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import os
import pandas as pd

from functions.get_url import get_url_categories
from functions.inicialitzar_driver import inicialitzar_driver
from functions.capta_url_seguent_pagina import capta_url_seguent_pagina
from functions.scrape_categoria_carrefour import scrape_categoria_carrefour

# Importem la funció get_category_url del mòdul functions
if __name__ == '__main__':
    #  Utilitzem la funció get_category_url
    print("Executant Extracció URL categories: Anàlisi de la pàgina font")

    # Guardem les categories amb la seva url a un fitxer csv
    categories_dict = get_url_categories()

    # 📊 Convertim el diccionari en un DataFrame
    df = pd.DataFrame(list(categories_dict.items()), columns=["Categoria", "URL"])

    # 💾 Guardem el DataFrame en un fitxer CSV
    output_path = 'data_scraped/url_categories_scraped.csv'
    df.to_csv(output_path, index=False, encoding='utf-8')

    print(f"✅ Dades desades a {output_path}")


    # Inicia el bucle iteratiu extern
    pagina = 1  # Primera execució
    url = "https://www.carrefour.es/supermercado/productos-frescos/cat20002/c"
    productes_totals = [] 
    response_delay = 1
    
    while pagina != 43:
        if os.path.exists("ultima_pagina_visitada.txt"):
            with open("ultima_pagina_visitada.txt", "r", encoding="utf-8") as file:
                lines = [line.rstrip() for line in file]
            pagina = int(lines[0])  # Última pàgina registrada
            url = lines[1]  # Última URL capturada
            time.sleep(10*response_delay)

        try:
            while url:
                t0 = time.time()
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
                productes = scrape_categoria_carrefour(driver, pagina, url)
                productes_totals.extend(productes)

                # Obtenir la URL de la següent pàgina
                soup = BeautifulSoup(driver.page_source, "html.parser")
                time.sleep(3)  # Una altra petita pausa per assegurar que el DOM és estable
                response_delay = time.time() - t0
                url = capta_url_seguent_pagina(soup)
                pagina += 1  # Incrementem el número de pàgina

                # Tanca el driver abans de continuar
                driver.quit()
                print("🌐 Connexió amb el servidor interrompuda per evitar detecció.")
                time.sleep(response_delay)
        except:
            print(f"⚠️ Error inesperat, reiniciant en l'última pàgina ({pagina}): {Exception}")
    
    if pagina == 43:
        print("✅ Finalització de l'scraping.")
        # Assegurem que el driver es tanca si hi ha errors
        try:
            driver.quit()
        except:
            pass

    # Guarda DataFrame
    os.makedirs("data_scraped", exist_ok=True)
    df = pd.DataFrame(productes_totals)
    print(len(df), df.size)
    df.to_csv("data_scraped/carrefour_products.csv", index=False)

    print(f"\n✅ Scraping complet: {len(productes_totals)} productes capturats.")
