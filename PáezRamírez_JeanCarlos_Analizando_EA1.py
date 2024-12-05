from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import csv
import os
import time
import random

def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59"
    ]
    return random.choice(user_agents)

def scrape_data():
    # Configuración del navegador
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome-stable"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent={get_random_user_agent()}")

    # Configuraciones adicionales para evitar detección
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # Configurar el servicio
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Modificar el navigator.webdriver
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # URL del producto
    url = 'https://www.amazon.com/-/es/Xiaomi-Smart-Band-Global-Version/dp/B0CD2MP728/'

    try:
        print("Iniciando extracción de datos...")

        # Añadir delay aleatorio antes de cargar la página
        time.sleep(random.uniform(2, 5))
        driver.get(url)

        # Esperar un tiempo aleatorio después de cargar la página
        time.sleep(random.uniform(3, 7))

        print("Página cargada. Intentando extraer datos...")

        # Extraer título
        try:
            title_element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, 'productTitle'))
            )
            title = title_element.text.strip()
            print(f"Título extraído: {title}")
        except TimeoutException:
            print("Tiempo de espera agotado al buscar el título")
            title = "Título no disponible"
        except Exception as e:
            print(f"Error al extraer título: {str(e)}")
            title = "Error en título"

        # Extraer precio
        price = "Precio no disponible"
        price_selectors = [
            (By.CLASS_NAME, 'a-price-whole'),
            (By.ID, 'priceblock_ourprice'),
            (By.ID, 'priceblock_dealprice'),
            (By.CLASS_NAME, 'a-price')
        ]

        for selector in price_selectors:
            try:
                price_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(selector)
                )
                price = price_element.text.strip()
                print(f"Precio extraído: {price}")
                break
            except:
                continue

        # Añadir extracción de rating
        try:
            rating_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'span[class*="a-icon-alt"]'))
            )
            rating = rating_element.get_attribute('innerHTML').split(' de ')[0]
            print(f"Rating extraído: {rating}")
        except:
            rating = "N/A"
            print("Rating no encontrado")

        # Añadir extracción de número de reviews
        try:
            reviews_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'acrCustomerReviewText'))
            )
            reviews = reviews_element.text.split(' ')[0]
            print(f"Número de reviews extraído: {reviews}")
        except:
            reviews = "0"
            print("Número de reviews no encontrado")

        # Guardar detalles en archivo de texto
        with open('product_details.txt', 'w', encoding='utf-8') as f:
            f.write(f"Título: {title}\n")
            f.write(f"Precio: {price}\n")
            f.write(f"Rating: {rating}\n")
            f.write(f"Número de Reviews: {reviews}\n")

        # Guardar datos en CSV
        output_file = os.path.join(os.getcwd(), 'output.csv')
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Price', 'Rating', 'Number_of_Reviews'])
            writer.writerow([title, price, rating, reviews])

        print(f"Datos guardados en {output_file}")
        print(f"Detalles guardados en {os.getcwd()}/product_details.txt")

        # Tomar captura de pantalla del éxito
        driver.save_screenshot('success_screenshot.png')
        print("Captura de pantalla guardada como success_screenshot.png")

    except Exception as e:
        print(f"Error al extraer datos: {str(e)}")
        driver.save_screenshot('error_screenshot.png')
        print("Captura de pantalla del error guardada como error_screenshot.png")
        raise

    finally:
        print("Cerrando el navegador...")
        driver.quit()