from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
import os

def scrape_data():
    # Configuración del navegador Brave (si Brave no está disponible, cambiar a Chrome)
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome-stable"  # Cambiar a Chrome si Brave no está disponible
    chrome_options.add_argument("--headless")  # Modo sin interfaz gráfica
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Usar WebDriver Manager para obtener el chromedriver
    service = Service(ChromeDriverManager().install())  # Esto instalará y obtendrá la ruta del WebDriver automáticamente
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # URL del producto en Amazon
    url = 'https://www.amazon.com/-/es/actividad-resoluci%C3%B3n-deportivos-frecuencia-inteligente/dp/B0B2DK5YCP'
    driver.get(url)

    try:
        # Extraer el título del producto
        title_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'productTitle'))
        )
        title = title_element.text.strip()

        # Extraer el precio del producto
        price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'a-price-whole'))
        )
        price = price_element.text.strip()

        # Ruta absoluta para guardar el archivo CSV
        output_file = os.path.join(os.getcwd(), 'output.csv')  # Usamos el directorio actual
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Price'])  # Encabezados
            writer.writerow([title, price])     # Datos extraídos

        # Confirmar que el archivo fue creado
        if os.path.exists(output_file):
            print(f"El archivo {output_file} fue creado exitosamente.")
        else:
            print(f"El archivo {output_file} no se pudo crear.")

    except Exception as e:
        print(f"Error al extraer datos: {e}")

    finally:
        # Cerrar el navegador
        driver.quit()

if __name__ == "__main__":
    scrape_data()


