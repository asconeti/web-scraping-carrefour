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
