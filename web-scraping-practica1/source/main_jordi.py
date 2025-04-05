
import pandas as pd
import os

from funcions_proba_DEFINITIU import  get_categories_pop, scrape_categoria


if __name__ == '__main__':

   
    #  Utilitzem la funció get_category_url
    print("Executant Extracció URL categories: Anàlisi de la pàgina font")

    # Guardem les categories amb la seva URL inicial, el número de productes i pàgines a un fitxer CSV
    categories_dict = get_categories_pop()


    # 📊 Convertim el diccionari en un DataFrame
    df = pd.DataFrame.from_dict(categories_dict, orient="index").reset_index()
    df.rename(columns={"index": "Nom de categoria"}, inplace=True)

    # Ruta del fitxer CSV
    output_path = 'data_scraped/categories_scraped.csv'

    # 💾 Assegurem-nos que la carpeta existeix
    output_dir = os.path.dirname(output_path)  # Obtenim la carpeta
    if not os.path.exists(output_dir):  # Comprovem si no existeix
        os.makedirs(output_dir)  # Creem la carpeta
        print(f"📁 Carpeta creada: {output_dir}")

    # Guardem el DataFrame en un fitxer CSV
    df.to_csv(output_path, index=False, encoding='utf-8')

    print(f"✅ Dades desades a {output_path}")
    

    # Inicialitzem les variables de suma
    total_productes = df["Número de productes"].sum()  # Suma total de productes
    total_productes_processats = 0
    total_productes_no_processats = 0

    print(f"🔢 Total de productes identificats: {total_productes}")

    # Bucle per iterar per cada categoria i executar scrape_categoria
    for _, row in df.iterrows():
        categoria = row["Nom de categoria"]
        url = row["URL"]
        productes_categoria = row["Número de productes"]
        pagines_categoria = row["Número de pàgines"]

        print(f"🛒 Processant categoria: {categoria}")
        
        try:
            # Crida a la funció scrape_categoria
            productes_processats = scrape_categoria(url, categoria, productes_categoria, pagines_categoria)
            total_productes_processats += productes_processats
            print(f"✅ Categoria '{categoria}' processada amb {productes_processats} productes.")
        except Exception as e:
            total_productes_no_processats += productes_categoria
            print(f"⚠️ Error processant la categoria '{categoria}': {e}")

    # Missatge final amb el resultat del processament
    print(f"🔢 Total de productes processats: {total_productes_processats}") # REVISAR
    print(f"🔢 Total de productes no processats: {total_productes_no_processats}") # REVISAR

