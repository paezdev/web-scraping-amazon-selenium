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
    # Configuración del navegador (Brave o Chrome)
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome-stable"  # Cambiar a Brave si es necesario
    chrome_options.add_argument("--headless")  # Modo sin interfaz gráfica
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    # Configuración del WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # URL del producto en Amazon
    url = 'https://www.amazon.com/-/es/Xiaomi-Smart-Band-Global-Version/dp/B0CD2MP728/ref=sr_1_1?sr=8-1'
    driver.get(url)

    try:
        print("Iniciando extracción de datos...")

        # Extraer el título del producto
        title_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'productTitle'))
        )
        title = title_element.text.strip()
        print(f"Título del producto: {title}")

        # Extraer el precio del producto
        price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'a-price-whole'))
        )
        price = price_element.text.strip()
        print(f"Precio del producto: {price}")

        # Ruta absoluta para guardar el archivo CSV
        output_file = os.path.join(os.getcwd(), 'output.csv')

        # Escribir o actualizar datos en el archivo CSV
        file_exists = os.path.exists(output_file)
        with open(output_file, mode='a' if file_exists else 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Title', 'Price'])  # Encabezados
            writer.writerow([title, price])  # Datos extraídos

        print(f"Datos guardados exitosamente en {output_file}")

    except Exception as e:
        print(f"Error al extraer datos: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_data()