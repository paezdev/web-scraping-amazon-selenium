from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # Para gestionar el driver automáticamente
import csv

def scrape_data():
    # Configuración del navegador Brave
    chrome_options = Options()
    chrome_options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

    # Configuración del WebDriver usando webdriver_manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # URL del producto
    url = 'https://www.amazon.com/-/es/actividad-resoluci%C3%B3n-deportivos-frecuencia-inteligente/dp/B0B2DK5YCP'
    driver.get(url)

    try:
        # Extraer el título del producto
        title_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'productTitle'))
        )
        title = title_element.text

        # Extraer el precio del producto
        price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'a-price-whole'))
        )
        price = price_element.text

        # Guardar en un archivo CSV
        with open('output.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Price'])  # Encabezados
            writer.writerow([title, price])     # Datos extraídos

        print("Datos extraídos y guardados en output.csv")

    except Exception as e:
        print(f"Error al extraer datos: {e}")

    finally:
        # Cerrar el navegador
        driver.quit()

if __name__ == "__main__":
    scrape_data()