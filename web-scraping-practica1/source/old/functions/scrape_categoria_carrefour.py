from bs4 import BeautifulSoup

from functions.guardar_html_debug import guardar_html_debug

def scrape_categoria_carrefour(driver, pagina, url) -> list:
    """
    Escrapeja productes de la pàgina actual utilitzant el driver Selenium.
    Retorna una llista de productes capturats.
    """
    productes = []
    soup = BeautifulSoup(driver.page_source, "html.parser")
    guardar_html_debug(soup, pagina, url)  # Guarda l'HTML complet per debugging

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