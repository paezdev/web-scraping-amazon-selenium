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
    # Configuración del navegador Brave (si Brave no está disponible, cambiar a Chrome)
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome-stable"  # Cambiar a Chrome si Brave no está disponible
    chrome_options.add_argument("--headless")  # Modo sin interfaz gráfica
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Agregar un user-agent para evitar ser bloqueado
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    # Usar WebDriver Manager para obtener el chromedriver
    service = Service(ChromeDriverManager().install())  # Esto instalará y obtendrá la ruta del WebDriver automáticamente
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # URL del producto en Amazon
    url = 'https://www.amazon.com/-/es/Xiaomi-Smart-Band-Global-Version/dp/B0CD2MP728/ref=sr_1_1?sr=8-1'
    driver.get(url)

    try:
        print("Página cargada. Intentando extraer datos...")

        # Esperar a que el título esté presente en la página (20 segundos)
        title_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'productTitle'))
        )
        title = title_element.text.strip()  # Eliminar espacios adicionales

        # Verificar si se extrajo el título
        if not title:
            raise Exception("No se pudo extraer el título del producto.")
        
        print(f"Título extraído: {title}")
        
        # Extraer el precio del producto
        price_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'a-price-whole'))
        )
        price = price_element.text.strip()

        # Asegurarse de que el precio se guarda como string
        price = str(price)

        print(f"Precio extraído: {price}")

        # Ruta absoluta para guardar el archivo CSV
        output_file = os.path.join(os.getcwd(), 'output.csv')  # Usamos el directorio actual
        
        # Verificar si el archivo ya existe, si no, se crea uno nuevo
        if os.path.exists(output_file):
            print(f"El archivo {output_file} ya existe. Procediendo con la actualización.")
        else:
            print(f"Creando nuevo archivo: {output_file}")
        
        # Escribir los datos extraídos en el archivo CSV
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Price'])  # Encabezados
            writer.writerow([title, price])     # Datos extraídos

        # Confirmar que el archivo fue creado o actualizado
        if os.path.exists(output_file):
            print(f"El archivo {output_file} fue creado o actualizado exitosamente.")
        else:
            print(f"El archivo {output_file} no se pudo crear.")

    except Exception as e:
        print(f"Error al extraer datos: {e}")
        driver.save_screenshot('error_screenshot.png')  # Captura de pantalla en caso de error
        print("Captura de pantalla del error guardada como error_screenshot.png")

    finally:
        # Cerrar el navegador
        driver.quit()

if __name__ == "__main__":
    scrape_data()

