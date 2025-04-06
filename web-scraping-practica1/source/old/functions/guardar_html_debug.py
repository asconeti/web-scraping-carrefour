import os

def guardar_html_debug(soup, pagina, url):
    """
    Guarda l'HTML complet de la pàgina actual a un fitxer per a debugging.
    """
    os.makedirs("debug_html_1", exist_ok=True)  # Crea la carpeta si no existeix
    fitxer_path = f"debug_html_1/pagina_{pagina}.html"
    with open(fitxer_path, "w", encoding="utf-8") as fitxer:
        fitxer.write(soup.prettify())
    print(f"📝 HTML de la pàgina {pagina} guardat a {fitxer_path}")
    
    with open("ultima_pagina_visitada.txt", "w", encoding="utf-8") as file:
        file.write(f"{pagina}\n{url}")