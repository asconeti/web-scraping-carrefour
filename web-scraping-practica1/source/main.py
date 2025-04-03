
import pandas as pd
import os

from functions.get_url import get_url_categories


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
