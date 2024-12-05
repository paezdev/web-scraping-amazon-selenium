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
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
    ]
    return random.choice(user_agents)

def scrape_data():
    # Configuración del navegador
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome-stable"
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent={get_random_user_agent()}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--lang=es-ES")
    chrome_options.add_argument("--disable-gpu")

    # Configuraciones experimentales
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    })

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        print("Iniciando extracción de datos...")

        url = 'https://www.amazon.com/-/es/Xiaomi-Smart-Band-Global-Version/dp/B0CD2MP728/'
        driver.get(url)
        time.sleep(random.uniform(3, 5))

        # Selectores para el título
        title_selectors = [
            (By.ID, 'productTitle'),
            (By.CSS_SELECTOR, 'h1.a-size-large'),
            (By.CSS_SELECTOR, 'span#productTitle'),
            (By.XPATH, "//span[@id='productTitle']")
        ]

        # Extraer título
        title = "Título no disponible"
        for selector_type, selector in title_selectors:
            try:
                title_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((selector_type, selector))
                )
                title = title_element.text.strip()
                if title:
                    print(f"Título extraído: {title}")
                    break
            except:
                continue

        # Selectores para el precio
        price_selectors = [
            (By.CSS_SELECTOR, 'span.a-price-whole'),
            (By.CSS_SELECTOR, 'span.a-offscreen'),
            (By.CSS_SELECTOR, '#priceblock_ourprice'),
            (By.CSS_SELECTOR, '#priceblock_dealprice'),
            (By.CSS_SELECTOR, '.a-price .a-offscreen'),
            (By.XPATH, "//span[@class='a-price-whole']"),
            (By.XPATH, "//span[@class='a-offscreen'][contains(text(),'$')]")
        ]

        # Extraer precio
        price = "Precio no disponible"
        for selector_type, selector in price_selectors:
            try:
                price_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((selector_type, selector))
                )
                price = price_element.text.strip().replace('US$', '').replace(',', '').replace('$', '')
                if price:
                    print(f"Precio extraído: {price}")
                    break
            except:
                continue

        # Selectores para el rating
        rating_selectors = [
            (By.CSS_SELECTOR, 'span.a-icon-alt'),
            (By.CSS_SELECTOR, '#acrPopover .a-icon-alt'),
            (By.XPATH, "//span[@class='a-icon-alt'][contains(text(),'de 5')]"),
            (By.CSS_SELECTOR, 'i.a-icon-star .a-icon-alt')
        ]

        # Extraer rating
        rating = "N/A"
        for selector_type, selector in rating_selectors:
            try:
                rating_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((selector_type, selector))
                )
                rating_text = rating_element.get_attribute('innerHTML')
                rating = rating_text.split(' de ')[0].strip()
                if rating:
                    print(f"Rating extraído: {rating}")
                    break
            except:
                continue

        # Selectores para reviews
        review_selectors = [
            (By.ID, 'acrCustomerReviewText'),
            (By.CSS_SELECTOR, '#acrCustomerReviewText'),
            (By.XPATH, "//span[@id='acrCustomerReviewText']"),
            (By.CSS_SELECTOR, 'span[data-hook="total-review-count"]')
        ]

        # Extraer número de reviews
        reviews = "0"
        for selector_type, selector in review_selectors:
            try:
                reviews_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((selector_type, selector))
                )
                reviews = reviews_element.text.split(' ')[0].replace(',', '').replace('.', '')
                if reviews:
                    print(f"Número de reviews extraído: {reviews}")
                    break
            except:
                continue

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

if __name__ == "__main__":
    scrape_data()