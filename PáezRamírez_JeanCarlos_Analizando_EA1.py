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
    # Configuración del navegador con más opciones anti-detección
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome-stable"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(f"user-agent={get_random_user_agent()}")

    # Añadir más headers aleatorios
    chrome_options.add_argument("--accept-language=es-ES,es;q=0.9,en;q=0.8")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-running-insecure-content")

    # Configuraciones experimentales
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Modificar más propiedades del navegador para evitar detección
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['es-ES', 'es']})")

    try:
        print("Iniciando extracción de datos...")

        # Añadir delays más naturales y aleatorios
        time.sleep(random.uniform(3, 7))

        # URL del producto
        url = 'https://www.amazon.com/-/es/Xiaomi-Smart-Band-Global-Version/dp/B0CD2MP728/'
        driver.get(url)

        # Simular comportamiento humano
        for _ in range(3):
            driver.execute_script(f"window.scrollTo(0, {random.randint(300, 700)});")
            time.sleep(random.uniform(1, 3))

        print("Página cargada. Intentando extraer datos...")

        # Verificar si hay CAPTCHA
        if "robot" in driver.page_source.lower() or "captcha" in driver.page_source.lower():
            print("CAPTCHA detectado - Esperando más tiempo...")
            time.sleep(random.uniform(10, 15))
            driver.refresh()
            time.sleep(random.uniform(5, 8))

        # Extraer título con múltiples intentos
        title = "Título no disponible"
        for _ in range(3):
            try:
                title_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'productTitle'))
                )
                title = title_element.text.strip()
                print(f"Título extraído: {title}")
                break
            except:
                time.sleep(random.uniform(2, 4))
                continue

        # Extraer precio con múltiples intentos
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

        # Extraer rating
        rating = "N/A"
        try:
            rating_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'span[class*="a-icon-alt"]'))
            )
            rating = rating_element.get_attribute('innerHTML').split(' de ')[0]
            print(f"Rating extraído: {rating}")
        except:
            print("Rating no encontrado")

        # Extraer número de reviews
        reviews = "0"
        try:
            reviews_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'acrCustomerReviewText'))
            )
            reviews = reviews_element.text.split(' ')[0]
            print(f"Número de reviews extraído: {reviews}")
        except:
            print("Número de reviews no encontrado")

        # Guardar detalles en archivo de texto
        with open('product_details.txt', 'w', encoding='utf-8') as f:
            f.write(f"Título: {title}\n")
            f.write(f"Precio: {price}\n")
            f.write(f"Rating: {rating}\n")
            f.write(f"Número de Reviews: {reviews}\n")

        # Guardar en CSV
        with open('output.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Price', 'Rating', 'Number_of_Reviews'])
            writer.writerow([title, price, rating, reviews])

        print(f"Datos guardados en {os.getcwd()}/output.csv")
        print(f"Detalles guardados en {os.getcwd()}/product_details.txt")

        # Tomar captura de pantalla
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

def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
    ]
    return random.choice(user_agents)