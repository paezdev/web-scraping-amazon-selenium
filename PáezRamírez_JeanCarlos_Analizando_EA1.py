from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
import os
import time

def scrape_data():
    # Configuración del navegador Brave o Chrome
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome-stable"  # Ajustar si usas Brave
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    # Quitar el comentario para probar sin headless si falla
    chrome_options.add_argument("--headless")

    # Agregar un user-agent personalizado para evitar bloqueos
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    # Usar WebDriver Manager para configurar el driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # URL del producto en Amazon
    url = 'https://www.amazon.com/-/es/Xiaomi-Smart-Band-Global-Version/dp/B0CD2MP728/ref=sr_1_1?sr=8-1'
    driver.get(url)
    print("Página cargada. Intentando extraer datos...")

    try:
        # Capturar captura de pantalla para depuración
        driver.save_screenshot("debug_screenshot.png")
        print("Captura de pantalla guardada como debug_screenshot.png")

        # Esperar y extraer el título del producto
        print("Esperando el título del producto...")
        title_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'productTitle'))
        )
        title = title_element.text.strip()
        print(f"Título encontrado: {title}")

        # Esperar y extraer el precio del producto
        print("Esperando el precio del producto...")
        price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'a-price-whole'))
        )
        price = price_element.text.strip()
        print(f"Precio encontrado: {price}")

        # Ruta absoluta para guardar el archivo CSV
        output_file = os.path.join(os.getcwd(), 'output.csv')
        
        # Verificar si el archivo ya existe
        if os.path.exists(output_file):
            print(f"El archivo {output_file} ya existe. Procediendo con la actualización.")
        else:
            print(f"Creando nuevo archivo: {output_file}")

        # Escribir los datos extraídos en el archivo CSV
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Price'])  # Encabezados
            writer.writerow([title, price])     # Datos extraídos

        print(f"Datos guardados en {output_file}")

    except Exception as e:
        print(f"Error al extraer datos: {e}")
        # Captura de pantalla adicional si ocurre un error
        driver.save_screenshot("error_screenshot.png")
        print("Captura de pantalla del error guardada como error_screenshot.png")

    finally:
        # Cerrar el navegador
        driver.quit()

if __name__ == "__main__":
    scrape_data()
