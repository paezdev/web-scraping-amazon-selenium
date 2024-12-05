import os
import pandas as pd
from PáezRamírez_JeanCarlos_Analizando_EA1 import scrape_data

def test_scraping_creates_files():
    # Ejecuta el scraping
    scrape_data()
    # Verifica que los archivos de salida existen
    assert os.path.exists("output.csv"), "El archivo CSV no fue creado"
    assert os.path.exists("product_details.txt"), "El archivo de detalles no fue creado"

def test_scraping_data_format():
    # Carga los datos del archivo CSV
    df = pd.read_csv("output.csv")
    # Verifica que el archivo no esté vacío
    assert not df.empty, "El archivo CSV está vacío"
    # Verifica que las columnas principales existan
    required_columns = ['Title', 'Price', 'Rating', 'Number_of_Reviews']
    for column in required_columns:
        assert column in df.columns, f"La columna '{column}' no está presente"

def test_scraping_non_empty_data():
    df = pd.read_csv("output.csv")
    # Verifica que los datos principales no estén vacíos
    assert df.iloc[0]["Title"].strip(), "El título del producto está vacío"
    assert str(df.iloc[0]["Price"]).strip(), "El precio del producto está vacío"

def test_product_details_file():
    # Verifica que el archivo de detalles tenga contenido
    assert os.path.getsize("product_details.txt") > 0, "El archivo de detalles está vacío"
