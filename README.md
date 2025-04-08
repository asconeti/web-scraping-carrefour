
**Integrants: Jordi Baiges Ferré & Ana Moscardó García** 

# 🛒 Web Scraping Carrefour - Pràctica 1 (Tipologia i cicle de vida de les dades - Màster en Ciència de dades)

## 📘 Introducció

Aquest projecte forma part de la pràctica 1 de l'assignatura *Tipologia i Cicle de Vida de les Dades* del Màster de Ciència de Dades de la UOC.

L'objectiu principal ha estat aplicar tècniques de **web scraping** amb **Selenium** i **BeautifulSoup** per extreure informació de productes del supermercat en línia de **Carrefour:(https://www.carrefour.es/supermercado)**.

S’han dissenyat funcions per automatitzar la navegació per les diferents categories, capturar la informació rellevant dels productes (nom, preus, imatges, promocions...), i transformar aquestes dades en formats estructurats (`CSV`).

Aquest projecte també explora la detecció i extracció de variables incrustades dins de codi JavaScript com `window["impressions"]`.

## 🚀 Guia d'ús

1. **Clonar el repositori:**

```bash
git clone https://github.com/usuari/exemple-repo.git
cd exemple-repo
```

2. **Executar dins un contenidor DevContainer (VSCode):**

   - Si utilitzes Windows i no tens **Docker** i **WSL2** instal·lats, VSCode t'ho demanarà.
   - L'entorn es crearà automàticament i els `requirements.txt` s’instal·laran perquè estan definits dins `.devcontainer/devcontainer.json`.

3. **Executar el projecte:**

```bash
cd web-scraping-practica1
python source/main.py
```

## 📁 Estructura del projecte

```
WEB-SCRAPING-PRACTICA1-MAIN
│
├── __pycache__/
├── .devcontainer/
│
└── web-scraping-practica1/
    ├── dataset/
    │   ├── .gitkeep
    │   ├── carrefour_products.csv
    │   └── categories_scraped.csv
    │
    ├── debug_html/
    │   └── .gitkeep (si existeix)
    │
    ├── resultats_script_json/
    │   └── .gitkeep (si existeix)
    │
    ├── source/
    │   ├── __pycache__/
    │   ├── functions.py
    │   └── main.py
    │
    ├── LICENSE.TXT
    ├── README.md
    └── requirements.txt

```

### 🔍 Descripció de les funcions

- `main.py`: És el punt d’entrada. Crida `get_url_categories()` per obtenir totes les categories, i després `scrape_categoria_carrefour()` per fer l’scraping.

- `get_url_categories.py`: Accedeix al web de Carrefour i extreu totes les URL de categories de productes, retornant-les com a diccionari.

- `scrape_categoria_carrefour.py`: Navega dins d’una categoria, recorre totes les pàgines de productes evitant els “carousel”, i guarda la informació en un DataFrame + CSV.
## 🛡️ Llicència

Aquest projecte ha estat desenvolupat amb **finalitats exclusivament educatives** dins d’un entorn acadèmic (UOC). Tant el codi com les dades generades no poden ser utilitzades amb finalitats comercials ni redistribuïdes.

> 🔒 **Llicència seleccionada:** CC BY-NC-SA 4.0  
> *(Reconeixement - No Comercial - Compartir Igual)*  
> https://creativecommons.org/licenses/by-nc-sa/4.0/



- `Zenodo DOI`: 10.5281/zenodo.15177237
- `Zenodo Link`:https://zenodo.org/records/15177237?token=eyJhbGciOiJIUzUxMiJ9.eyJpZCI6ImJjNDMyNzk2LTU3MDYtNDRmNi05MTgwLTVjM2JlYTZmNTI2MiIsImRhdGEiOnt9LCJyYW5kb20iOiI3N2NkMGMzZjdhMGZhZjUyNjM5YzFhZDRjMTdlZWYzZCJ9.veUuW_mc2pTEkN1XrclQCm7ZoOrXRTF2ae5ImbzRT2WWsTs3bGAfZfmRY45c7wAXP2vzXmA3fSNlggsvJ6w9aA

## 👨‍💻 Crèdits

Projecte desenvolupat per:

**Jordi Baiges Ferré i Ana Moscardó García**  
Estudiant del *Màster Universitari en Ciència de Dades*  
Universitat Oberta de Catalunya (UOC)  
2025

Professora : **Mireia Calvo González**

