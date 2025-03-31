# Orbea Monegros 2024 - PAC4

Aquest projecte consisteix en diverses funcions i tests per analitzar i processar dades de la cursa Orbea Monegros 2024. A continuació es descriuen les funcions implementades, els tests associats i com executar-los.

---

## **Requisits previs**
Abans d'executar qualsevol script o test, assegureu-vos d'instal·lar els requeriments necessaris:
```bash
pip install -r requirements.txt
```

> **Nota:** Totes les execucions del `main`, dels scripts dels exercicis i dels tests s'han de fer des de la consola situats al directori arrel de la carpeta del projecte descomprimida.

---

## **Funcions**

### **Exercici 1: Anàlisi del dataset**
**Fitxer:** `utils/analitza_csv_ex1.py`
- Llegeix i analitza el dataset original.
- Mostra les columnes i els primers registres del dataset.
- Determina quants ciclistes van participar a la prova.

### **Exercici 2: Anonimització i neteja del dataset**
**Fitxer:** `utils/anonimitza_i_neteja_csv_ex2.py`
- Anonimitza els noms dels ciclistes.
- Elimina les files amb temps igual a `00:00:00`.
- Guarda el dataset netejat.

### **Exercici 3: Agrupament dels minuts i generació d'un histograma**
**Fitxer:** `utils/group_by_minutes_ex3.py`
- Agrupa els temps en intervals de 20 minuts.
- Genera i guarda un histograma en format PNG.

### **Exercici 4: Neteja de noms dels clubs ciclistes**
**Fitxer:** `utils/neteja_noms_clubs_ex4.py`
- Neteja i normalitza els noms dels clubs.
- Agrupa i ordena els clubs pel nombre de membres.

### **Exercici 5: Anàlisi del club UCSC**
**Fitxer:** `utils/analisis_ucsc_ex5.py`
- Filtra i analitza els ciclistes del club UCSC.
- Determina el millor ciclista del club i la seva posició en el total.

---

## **Tests**
Els tests asseguren que totes les funcions funcionen correctament i estan implementats a `testos/test_orbea.py`. Cada exercici té també tests dedicats.

---

## **Estructura del Projecte**
```
Orbea_Monegros_2024/
├── data/
│   ├── raw/
│   │   └── dataset.csv
│   ├── processed/
│       ├── dataset_processed_ex2.csv
│       ├── dataset_processed_ex3.csv
│       └── dataset_processed_ex4.csv
├── img/
│   └── histograma.png
├── testos/
│   ├── test_orbea.py
│   ├── test_ex1.py
│   ├── test_ex2.py
│   ├── test_ex3.py
│   ├── test_ex4.py
│   └── test_ex5.py
├── utils/
│   ├── analitza_csv_ex1.py
│   ├── anonimitza_i_neteja_csv_ex2.py
│   ├── group_by_minutes_ex3.py
│   ├── neteja_noms_clubs_ex4.py
│   └── analisis_ucsc_ex5.py
├── main.py
└── requirements.txt
```

---

## **Com executar el projecte**

### **Executar tot el projecte des del `main.py`:**
```bash
python main.py data/raw/dataset.csv
```

### **Executar tots els tests des del `main`:**
```bash
python -m unittest testos/test_orbea.py
```

---

## **Detall d'execució per exercicis i tests**

### **Exercici 1**
- **Executar directament la funció:**
  ```bash
  python utils/analitza_csv_ex1.py data/raw/dataset.csv
  ```
- **Executar els tests:**
  ```bash
  python -m unittest testos/test_ex1.py
  ```

### **Exercici 2**
- **Executar directament la funció:**
  ```bash
  python utils/anonimitza_i_neteja_csv_ex2.py data/raw/dataset.csv data/processed/dataset_processed_ex2.csv
  ```
- **Executar els tests:**
  ```bash
  python -m unittest testos/test_ex2.py
  ```

### **Exercici 3**
- **Executar directament la funció:**
  ```bash
  python utils/group_by_minutes_ex3.py data/raw/dataset.csv data/processed/dataset_processed_ex3.csv img/histograma.png
  ```
- **Executar els tests:**
  ```bash
  python -m unittest testos/test_ex3.py
  ```

### **Exercici 4**
- **Executar directament la funció:**
  ```bash
  python utils/neteja_noms_clubs_ex4.py data/raw/dataset.csv data/processed/dataset_processed_ex4.csv
  ```
- **Executar els tests:**
  ```bash
  python -m unittest testos/test_ex4.py
  ```

### **Exercici 5**
- **Executar directament la funció:**
  ```bash
  python utils/analisis_ucsc_ex5.py data/processed/dataset_processed_ex4.csv
  ```
- **Executar els tests:**
  ```bash
  python -m unittest testos/test_ex5.py
  
