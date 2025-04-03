# Aquesta funcio ens serveix per guardar una copia del fitxer manipulat
import pandas as pd

def guarda_csv(df, nom_fitxer_sortida):
    """
    Guarda el dataframe en un fitxer CSV.
    """
    df.to_csv(nom_fitxer_sortida, index=False)
    print(f"Dataset guardat a: {nom_fitxer_sortida}")

"""
exercici_1:
desde la directory principal: Orbea_Monegros_2024 podem cridar a la funció


python utils/function_ex1.py data/raw/dataset.csv
"""
# DEPENDENCIES DE REQUIREMENTS:
# pip install pandas
# pip install faker
# pip install matplotlib

# per coneixer les versions instalades:
# pip show faker


# EXECUTEM TOT L'EXERCICI DESDE EL MAIN:
# python main.py data/raw/dataset.csv

# EXECUTEM TOTS ELS TESTOS DESDE EL MAIN:
# python -m unittest testos/test_orbea.py


# Executem EX1 cridant directament a la funcio, des-de el directori arrel:
# python utils/analitza_csv_ex1.py data/raw/dataset.csv

# Executem TEST_1 de l'exercici_1
# python -m unittest testos/test_ex1.py

# Executem EX2 cridant directament a la funcio, des-de el directori arrel:
# python utils/anonimitza_i_neteja_csv_ex2.py data/raw/dataset.csv data/processed/dataset_processed_ex2.csv

# Executem TEST_2 de l'exercici_2
# python -m unittest testos/test_ex2.py

# Executem EX3 cridant directament a la funcio, des-de el directori arrel:
# python utils/group_by_minutes_ex3.py data/raw/dataset.csv data/processed/dataset_processed_ex3.csv img/histograma.png

# Executem TEST_3 de l'exercici_3
# python -m unittest testos/test_ex3.py

# Executem EX4 cridant directament a la funcio, des-de el directori arrel:
# python utils/neteja_noms_clubs_ex4.py data/raw/dataset.csv data/processed/dataset_processed_ex4.csv

# Executem TEST_4 de l'exercici_4
# python -m unittest testos/test_ex4.py

# Executem EX5 cridant directament a la funcio, des-de el directori arrel:
# python utils/analisis_ucsc_ex5.py data/processed/dataset_processed_ex4.csv

# Executem TEST_5 de l'exercici_5
# python -m unittest testos/test_ex5.py
