import os
import pandas as pd
from PáezRamírez_JeanCarlos_Analizando_EA1 import scrape_data

def test_scraping_creates_file():
    # Ejecuta el scraping
    scrape_data()
    # Verifica que el archivo de salida existe
    assert os.path.exists("output.csv"), "El archivo de salida no fue creado"

def test_scraping_data_format():
    # Carga los datos del archivo generado
    df = pd.read_csv("output.csv")
    # Verifica que el archivo no esté vacío
    assert not df.empty, "El archivo de salida está vacío"
    # Verifica que las columnas esperadas existan
    assert "Title" in df.columns, "La columna 'Title' no está presente"
    assert "Price" in df.columns, "La columna 'Price' no está presente"

def test_scraping_non_empty_data():
    # Verifica que los datos extraídos no estén vacíos
    df = pd.read_csv("output.csv")
    assert df.iloc[0]["Title"].strip(), "El título del producto está vacío"
    
    # Asegurarse de que 'Price' es tratado como cadena antes de aplicar .strip()
    assert str(df.iloc[0]["Price"]).strip(), "El precio del producto está vacío"

