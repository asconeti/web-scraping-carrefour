from playwright.sync_api import sync_playwright
import pandas as pd
import time
import random


def scrape_categoria_carrefour(url_categoria: str) -> pd.DataFrame:
    """
    Utilitza Playwright per navegar i capturar informació de productes d'una categoria de Carrefour,
    incloent l'acceptació de cookies, el tancament de finestres emergents inicials i simulacions humanes.
    """
    productes = []
    pagina = 1

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
        page = context.new_page()

        # Carrega la primera pàgina
        page.goto(url_categoria)
        time.sleep(random.uniform(3, 6))  # Pausa aleatòria per simular un comportament humà

        # Accepta cookies
        try:
            cookies_button = page.query_selector("text='I Accept'")
            if cookies_button and cookies_button.is_visible():
                print("➡️ Acceptant cookies...")
                cookies_button.hover()
                time.sleep(random.uniform(1, 3))  # Pausa aleatòria abans de clicar
                cookies_button.click()
                time.sleep(random.uniform(2, 5))
            else:
                print("📌 Botó d'acceptació de cookies no trobat.")
        except Exception as e:
            print(f"⚠️ Problema al gestionar les cookies: {e}")

        # Tanca la finestra emergent inicial
        try:
            popup_close_button = page.query_selector("text='EMPEZAR'")
            if popup_close_button and popup_close_button.is_visible():
                print("➡️ Tancant finestra emergent inicial...")
                popup_close_button.hover()
                time.sleep(random.uniform(1, 3))
                popup_close_button.click()
                time.sleep(random.uniform(2, 5))
            else:
                print("📌 Finestra emergent inicial no trobada.")
        except Exception as e:
            print(f"⚠️ Problema al gestionar la finestra emergent inicial: {e}")

        while True:
            print(f"➡️ Processant pàgina {pagina}: {page.url}")

            # Espera que els productes es carreguin
            try:
                page.wait_for_selector(".product-card-list__item", timeout=20000)
                time.sleep(random.uniform(1, 3))  # Pausa per simular espera humana
            except Exception:
                print("⚠️ Els productes no s'han carregat correctament.")
                break

            # Scroll incremental profund amb moviments del ratolí
            print("📜 Realitzant scroll incremental profund amb interaccions...")
            for _ in range(15):  # Desplaça més profundament
                page.evaluate("window.scrollBy(0, window.innerHeight / 2)")
                x = random.randint(100, 500)  # Moviments aleatoris
                y = random.randint(100, 500)
                page.mouse.move(x, y)
                time.sleep(random.uniform(2, 4))  # Pausa aleatòria
            print("📜 Scroll completat!")

            # Captura dels productes
            productes_html = page.query_selector_all(".product-card-list__item")
            for producte in productes_html:
                try:
                    descripcio = producte.query_selector(".product-card__title-link").inner_text() or ""
                    preu_unitari = producte.query_selector(".product-card__price").inner_text() or ""
                    preu_kg = (
                        producte.query_selector(".product-card__price-per-unit").inner_text()
                        if producte.query_selector(".product-card__price-per-unit")
                        else ""
                    )
                    url_producte = producte.query_selector(".product-card__title-link").get_attribute("href") or ""
                    url_producte = f"https://www.carrefour.es{url_producte}"

                    imatge = (
                        producte.query_selector("img").get_attribute("src")
                        if producte.query_selector("img")
                        else ""
                    )

                    productes.append({
                        "Descripció": descripcio.strip(),
                        "Preu unitari": preu_unitari.strip(),
                        "Preu/kg": preu_kg.strip(),
                        "URL": url_producte.strip(),
                        "Imatge": imatge.strip(),
                    })

                    print(f"✅ Producte capturat: {descripcio}")

                except Exception as e:
                    print(f"⚠️ Error capturant un producte: {e}")

            # Desplaçament precís i clic al botó "Página siguiente"
            try:
                next_button = page.query_selector(
                    "#app > div > main > div.plp-food-view__main > div.plp-food-view__container > div > div.plp-food-view__list > div.plp-food-view__results-list-container > div.plp-food-view__pagination > div > div.pagination__container > div > a"
                )
                if next_button and next_button.is_visible():
                    print("➡️ Desplaçant el ratolí al botó de pàgina següent...")
                    box = next_button.bounding_box()  # Obté les coordenades del botó
                    if box:
                        x_center = box["x"] + box["width"] / 2
                        y_center = box["y"] + box["height"] / 2
                        page.mouse.move(x_center, y_center)
                        time.sleep(random.uniform(1, 3))
                        page.mouse.click(x_center, y_center)  # Fes clic amb les coordenades del botó
                        time.sleep(random.uniform(10, 15))  # Pausa més llarga per simular espera humana
                        pagina += 1
                    else:
                        print("❌ No s'han pogut obtenir les coordenades del botó.")
                        break
                else:
                    print("📌 Botó 'Página siguiente' no disponible. Finalitzant scraping.")
                    break
            except Exception as e:
                print(f"❌ Error al passar de pàgina: {e}")
                break

        # Tanca el navegador
        browser.close()

    # Guarda els resultats en un CSV
    df = pd.DataFrame(productes)
    df.to_csv("data_scraped/carrefour_products.csv", index=False)
    print(f"✅ Scraping complet: {len(productes)} productes capturats.")
    return df


# Exemple d'ús
url = "https://www.carrefour.es/supermercado/productos-frescos/cat20002/c"
df = scrape_categoria_carrefour(url)
