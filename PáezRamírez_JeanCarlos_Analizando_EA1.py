import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_data():
    """Función para extraer datos de Amazon y guardarlos en archivos CSV y de texto."""

    # Configuración de WebDriver para Brave Browser
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecutar sin interfaz gráfica
    chrome_options.add_argument("--no-sandbox")  # Requerido para entornos CI
    chrome_options.add_argument("--disable-dev-shm-usage")  # Optimización para entornos CI
    chrome_options.add_argument("--remote-debugging-port=9222")  # Depuración remota

    # Especifica la ruta al ejecutable de Brave (por defecto suele estar en /usr/bin/brave-browser en entornos CI)
    chrome_options.binary_location = "/usr/bin/brave-browser"

    # Usamos el WebDriver de Chrome pero apuntando a Brave
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    url = 'https://www.amazon.com/-/es/inteligente-frecuencia-Bluetooth-deportivo-M2239B1/dp/B0C3B42Q29'
    data = []

    try:
        driver.get(url)
        driver.maximize_window()

        # Espera explícita para asegurarse de que el título del producto esté cargado
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'productTitle')))

        # Extraemos el título del producto
        try:
            title = driver.find_element(By.ID, 'productTitle').text
        except Exception as e:
            title = "No encontrado"

        # Extraemos el precio del producto
        try:
            price_whole = driver.find_element(By.CLASS_NAME, 'a-price-whole').text
            price_fraction = driver.find_element(By.CLASS_NAME, 'a-price-fraction').text
            price = f"US${price_whole}.{price_fraction}"
        except Exception as e:
            price = "No disponible"

        # Extraemos el rating del producto (en formato decimal)
        try:
            rating = driver.find_element(By.CLASS_NAME, 'a-icon-alt').text
            # Extraemos el valor numérico del rating
            rating_value = rating.split(" ")[0]  # Obtiene la primera parte antes de "de 5 estrellas"
        except Exception as e:
            rating_value = "No disponible"

        # Extraemos las características clave (especificaciones)
        try:
            features = driver.find_element(By.ID, 'feature-bullets').text
        except Exception as e:
            features = "No disponibles"
        
        # Extraemos el número de reseñas
        try:
            reviews = driver.find_element(By.ID, 'acrCustomerReviewText').text
        except Exception as e:
            reviews = "No disponibles"

        # Guardamos los datos extraídos en un diccionario
        data.append({
            'Title': title,
            'Price': price,
            'Rating': rating_value,
            'Features': features,
            'Number_of_Reviews': reviews  # Añadimos la columna de reseñas
        })

        # Guardamos los datos en un archivo CSV
        with open('output.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['Title', 'Price', 'Rating', 'Features', 'Number_of_Reviews'])
            writer.writeheader()
            writer.writerows(data)

        # Crear el archivo product_details.txt con los mismos datos
        with open('product_details.txt', mode='w', encoding='utf-8') as text_file:
            text_file.write(f"Title: {title}\n")
            text_file.write(f"Price: {price}\n")
            text_file.write(f"Rating: {rating_value}\n")
            text_file.write(f"Features: {features}\n")
            text_file.write(f"Number of Reviews: {reviews}\n")

        # Tomamos una captura de pantalla
        screenshot_path = 'success_screenshot.png'
        driver.save_screenshot(screenshot_path)

    except Exception as e:
        # Si ocurre un error, tomamos una captura de pantalla de la página de error
        error_screenshot_path = 'error_screenshot.png'
        driver.save_screenshot(error_screenshot_path)

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_data()
