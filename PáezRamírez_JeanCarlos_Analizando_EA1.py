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
    # Configuración del navegador
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome-stable"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = 'https://www.amazon.com/-/es/Xiaomi-Smart-Band-Global-Version/dp/B0CD2MP728/ref=sr_1_1?sr=8-1'
    driver.get(url)

    try:
        print("Página cargada. Intentando extraer datos...")

        # Dictionary para almacenar toda la información
        product_info = {}

        # Extraer título
        title_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'productTitle'))
        )
        product_info['Title'] = title_element.text.strip()

        # Extraer precio
        try:
            price_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'a-price-whole'))
            )
            product_info['Price'] = price_element.text.strip()
        except:
            product_info['Price'] = "Precio no disponible"

        # Extraer calificación
        try:
            rating_element = driver.find_element(By.ID, 'acrPopover')
            product_info['Rating'] = rating_element.get_attribute('title')
        except:
            product_info['Rating'] = "Calificación no disponible"

        # Extraer número de reseñas
        try:
            reviews_element = driver.find_element(By.ID, 'acrCustomerReviewText')
            product_info['Number_of_Reviews'] = reviews_element.text
        except:
            product_info['Number_of_Reviews'] = "Reseñas no disponibles"

        # Extraer disponibilidad
        try:
            availability_element = driver.find_element(By.ID, 'availability')
            product_info['Availability'] = availability_element.text.strip()
        except:
            product_info['Availability'] = "Disponibilidad no especificada"

        # Extraer detalles técnicos
        try:
            details_table = driver.find_element(By.ID, 'productDetails_techSpec_section_1')
            rows = details_table.find_elements(By.TAG_NAME, 'tr')
            for row in rows:
                try:
                    label = row.find_element(By.CLASS_NAME, 'label').text.strip()
                    value = row.find_element(By.CLASS_NAME, 'value').text.strip()
                    product_info[f"Spec_{label}"] = value
                except:
                    continue
        except:
            product_info['Technical_Details'] = "Detalles técnicos no disponibles"

        # Extraer descripción del producto
        try:
            description_element = driver.find_element(By.ID, 'productDescription')
            product_info['Description'] = description_element.text.strip()
        except:
            product_info['Description'] = "Descripción no disponible"

        # Extraer características principales (Bullet points)
        try:
            features_list = driver.find_element(By.ID, 'feature-bullets')
            features = features_list.find_elements(By.TAG_NAME, 'li')
            product_info['Features'] = [feature.text.strip() for feature in features]
        except:
            product_info['Features'] = "Características no disponibles"

        # Extraer información del vendedor
        try:
            seller_element = driver.find_element(By.ID, 'merchant-info')
            product_info['Seller_Info'] = seller_element.text.strip()
        except:
            product_info['Seller_Info'] = "Información del vendedor no disponible"

        # Guardar en CSV
        output_file = os.path.join(os.getcwd(), 'output.csv')

        # Escribir los datos extraídos en el archivo CSV
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Escribir encabezados
            writer.writerow(product_info.keys())
            # Escribir valores
            writer.writerow(product_info.values())

        print(f"Datos extraídos y guardados en {output_file}")

        # También guardar en formato más legible
        readable_output = os.path.join(os.getcwd(), 'product_details.txt')
        with open(readable_output, mode='w', encoding='utf-8') as file:
            for key, value in product_info.items():
                file.write(f"{key}:\n{value}\n\n")

        print(f"Detalles completos guardados en {readable_output}")

    except Exception as e:
        print(f"Error al extraer datos: {e}")
        driver.save_screenshot('error_screenshot.png')
        print("Captura de pantalla del error guardada como error_screenshot.png")

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_data()


