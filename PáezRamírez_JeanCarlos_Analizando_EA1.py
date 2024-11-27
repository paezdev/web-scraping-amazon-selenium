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
    
    # Agregar un user-agent para evitar ser bloqueado
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    # Usar WebDriver Manager para obtener el chromedriver
    service = Service(ChromeDriverManager().install())  # Esto instalará y obtendrá la ruta del WebDriver automáticamente
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # URL del producto en Amazon
    url = 'https://webscraper.io/test-sites/e-commerce/allinone/product/86'
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

        # Asegurarse de que el precio se guarda como string
        price = str(price)

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

    finally:
        # Cerrar el navegador
        driver.quit()

if __name__ == "__main__":
    scrape_data()

