# Importem les llibreries necessàries
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os
import sys
import pandas as pd
import random
import requests
from datetime import datetime


def numero_productes_i_pagines(soup):
    """
    Capturem el número de productes i pàgines de la categoría.
    Retorna una llista amb número de productes, pàgines o None si no s'ha trovat.
    """
    try:
        # Captura el número total de productes
        numero_productes = soup.find("div", class_="pagination__results").find_all("span", class_="pagination__results-item")[-1].text.strip()

        # Captura el número total de pàgines
        numero_pagines_text = soup.find("div", class_="pagination__main").text.strip()
        numero_pagines = int(numero_pagines_text.split(" ")[-1])  # Obtenim el número després de "de"

        print(f"➡️ Capturat el número de productes: {numero_productes}")
        print(f"➡️ Capturat el número de pàgines: {numero_pagines}")

        return int(numero_productes), numero_pagines

    except AttributeError:
        print("📌 No s'han trobat totes les dades de la categoria.")
        return None
    


def get_categories_pop():
    """
    Accedeix a la pàgina de Carrefour Supermercado, extreu les categories de productes
    (excloent "Mis productos" i "Ofertas") i retorna un diccionari amb el format:
    {"Nom de categoria": {"URL", "Número de productes", "Número de pàgines"}}
    
    Retorna:
        dict: Diccionari amb les categories, URL completes, número de productes i número de pàgines.
    """
    resultats = {}
    domini = "https://www.carrefour.es"

    try:
        print("🌐 Accedint a la pàgina principal de Carrefour Supermercado...")

        # Utilitza un nou driver per a la pàgina principal
        driver = inicialitzar_driver()
        driver.get(f"{domini}/supermercado")
        time.sleep(5)  # Espera perquè es carregui el contingut inicial
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        links = soup.select("a.nav-first-level-categories__list-element")
        driver.quit()  # Tanquem el driver després de processar la pàgina principal

        if not links:
            print("⚠️ No s'han trobat enllaços de categories.")
            return resultats

        # Processar cada enllaç de categoria
        for a in links:
            nom = a.get_text(strip=True)
            href = a.get("href")
            if nom.lower() not in ["mis productos", "ofertas"] and href:
                href_complet = domini + href if href.startswith("/") else href

                print(f"🔎 Processant categoria: {nom}")

                max_attempts = 2  # Número màxim d'intents
                attempts = 0
                success = False

                while attempts < max_attempts and not success:
                    # Reinicia el driver per a cada intent
                    driver = inicialitzar_driver()
                    try:
                        driver.get(href_complet)
                        print(f"🌐 Intent {attempts + 1} accedint a la categoria... {href_complet}")
                        time.sleep(5)

                        # Esperem que els productes es carreguin completament
                        try:
                            wait = WebDriverWait(driver, 20)
                            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-card-list__item")))
                        except:
                            print(f"⚠️ No s'han carregat completament els productes per a la categoria: {nom}")

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

                        # Processar HTML amb BeautifulSoup
                        soup = BeautifulSoup(driver.page_source, 'html.parser')

                        # Captura el número de productes i pàgines
                        dades = numero_productes_i_pagines(soup)
                        if dades:
                            numero_productes, numero_pagines = dades
                            resultats[nom] = {
                                "URL": href_complet,
                                "Número de productes": numero_productes,
                                "Número de pàgines": numero_pagines
                            }
                            success = True
                            print(f"✅ Dades capturades per la categoria: {nom}")
                        else:
                            print(f"⚠️ No s'han capturat dades per la categoria: {nom} en l'intent {attempts + 1}")

                    except Exception as e:
                        print(f"⚠️ Error durant l'intent {attempts + 1} per la categoria {nom}: {e}")

                    finally:
                        driver.quit()

                    attempts += 1

                if not success:
                    print(f"❌ No s'han pogut obtenir les dades per a la categoria {nom} després de {max_attempts} intents.")

        print(f"✅ Categories trobades: {len(resultats)}")

    except Exception as e:
        print(f"⚠️ Error: {e}")

    finally:
        try:
            driver.quit()
        except Exception as ex:
            print(f"⚠️ Error tancant el driver: {ex}")

    return resultats

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
    next_page_link = soup.find("link", {"rel": "next"})
    if next_page_link and next_page_link.get("href"):
        next_page_url = next_page_link.get("href")
        print(f"➡️ Capturada la URL de la següent pàgina: {next_page_url}")
        return next_page_url
    else:
        print("📌 No hi ha més pàgines disponibles.")
        return None



def guardar_html_debug(soup, pagina):
    """
    Guarda l'HTML complet de la pàgina actual a un fitxer per a debugging.
    """
    os.makedirs("debug_html", exist_ok=True)  # Crea la carpeta si no existeix
    fitxer_path = f"debug_html/pagina_{pagina}.html"
    with open(fitxer_path, "w", encoding="utf-8") as fitxer:
        fitxer.write(soup.prettify())
    print(f"📝 HTML de la pàgina {pagina} guardat a {fitxer_path}")
   


def scrape_pagina_pop(driver, pagina, categoria) -> list:
    """
    Escrapeja productes de la pàgina actual utilitzant el driver Selenium.
    Retorna una llista de productes capturats.
    """
    productes = []
    soup = BeautifulSoup(driver.page_source, "html.parser")  # Carreguem l'arbre jeràrquic a "soup"
    guardar_html_debug(soup, pagina)  # Guarda l'HTML complet per debugging

    target_li = soup.select("li.product-card-list__item")  # Identifiquem l'element objectiu

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

            # Camps habituals
            descripcio = titol_tag.get_text(strip=True) if titol_tag else ""
            preu_tag = li.select_one(".product-card__price")
            preu_unitari = preu_tag.get_text(strip=True) if preu_tag else ""
            preu_kg_tag = li.select_one(".product-card__price-per-unit")
            preu_kg = preu_kg_tag.get_text(strip=True) if preu_kg_tag else ""

            media_link_tag = li.select_one(".product-card__media-link")
            url_producte = f"https://www.carrefour.es{media_link_tag.get('href')}" if media_link_tag else ""

            img_tag = li.select_one("img")
            url_imatge = img_tag.get("src") if img_tag else ""

            # Camps nous
            badge_tag = li.select_one(".badge_name")
            promocio = badge_tag.get_text(strip=True) if badge_tag else ""

            preu_strikethrough_tag = li.select_one(".app_strikethrough_price")
            preu_unitari_pre_descompte = preu_strikethrough_tag.get_text(strip=True) if preu_strikethrough_tag else ""
            preu_kg_pre_descompte = preu_strikethrough_tag.get_text(strip=True) if preu_strikethrough_tag else ""

            disponibilitat_tag = li.select_one(".add-to-cart-button__button--sold-out")
            disponibilitat = disponibilitat_tag.get_text(strip=True) if disponibilitat_tag else "Disponible"

            caracteristiques_tags = li.select(".product-card__item-info-tag")
            caracteristiques = [tag.get_text(strip=True) for tag in caracteristiques_tags]

            hora_de_captura = datetime.now().strftime("%H:%M:%S")  # Hora, minut, segon de captura

            # Afegim info producte a la llista "productes"
            productes.append({
                "Hora de captura": hora_de_captura,
                "Categoria": categoria,  # Categoria a la qual pertany
                "Descripció": descripcio,
                "Preu unitari": preu_unitari,
                "Preu/kg": preu_kg,
                "URL": url_producte,
                "Imatge": url_imatge,
                "Promoció": promocio,
                "Preu unitari pre-descompte": preu_unitari_pre_descompte,
                "Preu/kg pre-descompte": preu_kg_pre_descompte,
                "Disponibilitat": disponibilitat,
                "Característiques": caracteristiques
            })


            print(f"✅ Producte capturat: {descripcio}")

        except Exception as e:
            print(f"⚠️ Error amb un producte: {e}")

    # Retorna la llista de productes capturats
    return productes


def scrape_categoria(url, categoria, productes_categoria, pagines_categoria):
    """
    Funció per escrapejar productes d'una categoria a partir de la URL.
    
    Paràmetres:
        url (str): URL de la categoria per escrapejar productes.
    
    Retorna:
        int: El nombre de productes escrapejats.
    """
    
    productes_totals_categoria = [] # inicialitzem la llista de productes categoria
    pagina = 1  # Iniciem la pàgina a 1

    try:
        while url:
        
            t0 = time.time()  # Ana - Record the starting time #################################################
            print(f"🔎 Processant URL: {url}")

            # Inicialitza un nou driver per cada pàgina
            driver = inicialitzar_driver() # Funció per inicialitzar el driver
            driver.get(url) # guardem l'html de la pàgina "url" damunt de "driver"
            time.sleep(5)  # Espera inicial abans d'interactuar amb la pàgina (comportament humà...)

            # Espera que la pàgina es carregui completament
            wait = WebDriverWait(driver, 20)
            # Esperem que l'etiqueta objectiu que conté els productes "product-card-list__item" estigui present
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


            # Funció principal: Escrapejar productes de la pàgina actual
            productes = scrape_pagina_pop(driver, pagina, categoria)

            # Afegim els productes capturats de la pàgina, a la llista total
            productes_totals_categoria.extend(productes)

            # Obtenir la URL de la següent pàgina
            soup = BeautifulSoup(driver.page_source, "html.parser")
            time.sleep(3)  # Una altra petita pausa per assegurar que el DOM és estable
            response_delay = time.time() - t0 # Ana ######################
            url = capta_url_seguent_pagina(soup) # Assignem url de la pàgina seguent
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
    # Crear carpeta si no existeix
    os.makedirs("data_scraped", exist_ok=True)

    # Convertir la llista de productes en un DataFrame
    df = pd.DataFrame(productes_totals_categoria)

    # Comprovar si el fitxer ja existeix
    file_path = "data_scraped/carrefour_products.csv"
    if not os.path.exists(file_path):
        # Si no existeix, guardar amb la capçalera
        df.to_csv(file_path, index=False)
    else:
        # Si existeix, afegir al fitxer sense capçalera
        df.to_csv(file_path, mode="a", header=False, index=False)


    print(f"\n✅ Scraping categoria complet: {len(productes_totals_categoria)} productes capturats.")


########################################################################################################

