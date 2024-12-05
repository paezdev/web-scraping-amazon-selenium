from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os


def scrape_data():
    """Función para extraer datos de Amazon y guardarlos en archivos CSV y de texto."""
    # Configuración de WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    url = 'https://www.amazon.com/-/es/Xiaomi-Smart-Band-Global-Version/dp/B0CD2MP728/'
    data = []

    try:
        driver.get(url)
        driver.maximize_window()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "productTitle")))

        # Extraer título
        try:
            title = driver.find_element(By.ID, "productTitle").text.strip()
        except:
            title = "Título no disponible"

        # Extraer precio
        try:
            price = driver.find_element(By.CSS_SELECTOR, "span.a-price").text.strip()
        except:
            price = "Precio no disponible"

        # Extraer rating
        try:
            rating = driver.find_element(By.CSS_SELECTOR, "span.a-icon-alt").text.strip()
        except:
            rating = "Rating no disponible"

        # Extraer número de reseñas
        try:
            reviews = driver.find_element(By.ID, "acrCustomerReviewText").text.strip()
        except:
            reviews = "Reseñas no disponibles"

        # Almacenar datos en una lista
        data.append({
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Number_of_Reviews": reviews
        })

        # Guardar en CSV
        df = pd.DataFrame(data)
        df.to_csv("output.csv", index=False)

        # Guardar en archivo de texto
        with open("product_details.txt", "w", encoding="utf-8") as f:
            f.write(f"Título: {title}\nPrecio: {price}\nRating: {rating}\nNúmero de reseñas: {reviews}\n")

        # Guardar captura de pantalla en caso de éxito
        driver.save_screenshot("success_screenshot.png")
        print("Datos extraídos correctamente.")

    except Exception as e:
        print(f"Error durante la extracción: {e}")
        driver.save_screenshot("error_screenshot.png")
    finally:
        driver.quit()


if __name__ == "__main__":
    scrape_data()
