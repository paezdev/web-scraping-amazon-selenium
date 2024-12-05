import os
import pandas as pd
from PáezRamírez_JeanCarlos_Analizando_EA1 import scrape_data

def test_scraping_creates_files():
    try:
        scrape_data()
        assert os.path.exists("output.csv"), "El archivo CSV no fue creado"
        assert os.path.exists("product_details.txt"), "El archivo de detalles no fue creado"
    except Exception as e:
        print(f"Error durante el scraping: {str(e)}")
        raise

def test_scraping_data_format():
    try:
        df = pd.read_csv("output.csv")
        assert not df.empty, "El archivo CSV está vacío"
        required_columns = ['Title', 'Price', 'Rating', 'Number_of_Reviews']
        for column in required_columns:
            assert column in df.columns, f"La columna '{column}' no está presente"
    except Exception as e:
        print(f"Error al verificar el formato de datos: {str(e)}")
        raise

def test_scraping_non_empty_data():
    try:
        df = pd.read_csv("output.csv")
        assert df.iloc[0]["Title"].strip(), "El título del producto está vacío"
        assert str(df.iloc[0]["Price"]).strip(), "El precio del producto está vacío"
    except Exception as e:
        print(f"Error al verificar datos no vacíos: {str(e)}")
        raise

def test_product_details_file():
    try:
        assert os.path.exists("product_details.txt"), "El archivo de detalles no existe"
        assert os.path.getsize("product_details.txt") > 0, "El archivo de detalles está vacío"
    except Exception as e:
        print(f"Error al verificar archivo de detalles: {str(e)}")
        raise