import time
import json
import logging
from datetime import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configuración del logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ===== FUNCIONES =====

def autenticar_google_sheets():
    SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    with open("credentials.json") as f:
        creds_data = json.load(f)
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_data, SCOPES)
    client = gspread.authorize(credentials)
    sheet = client.open("resultados tracking").sheet1
    return sheet

def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def extraer_ofertas(driver):
    url = "https://www.mercadolibre.com.mx/ofertas#nav-header"
    driver.get(url)
    time.sleep(3)  # Espera para carga completa

    productos = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    items = driver.find_elements(By.CSS_SELECTOR, 'a.poly-component__title')
    precios_actuales = driver.find_elements(By.CSS_SELECTOR, 'div.poly-price__current span.andes-money-amount__fraction')
    precios_anteriores = driver.find_elements(By.CSS_SELECTOR, 's.andes-money-amount--previous span.andes-money-amount__fraction')

    for i in range(len(items)):
        nombre = items[i].text.strip()
        enlace = items[i].get_attribute("href")
        precio_actual = precios_actuales[i].text if i < len(precios_actuales) else "No disponible"
        precio_anterior = precios_anteriores[i].text if i < len(precios_anteriores) else "Sin descuento"

        productos.append([timestamp, nombre, precio_actual, precio_anterior, enlace])
        logging.info(f"{nombre} - {precio_actual} MXN (antes: {precio_anterior})")

    return productos

def guardar_en_sheets(sheet, datos):
    if datos:
        sheet.append_rows(datos)
        logging.info(f"📌 {len(datos)} productos guardados en Google Sheets.")
    else:
        logging.warning("No se encontraron productos para guardar.")

# ===== EJECUCIÓN PRINCIPAL =====

def main():
    hoja = autenticar_google_sheets()
    
    while True:
        logging.info("🔍 Iniciando proceso de scraping...")
        driver = iniciar_driver()

        try:
            productos = extraer_ofertas(driver)
            guardar_en_sheets(hoja, productos)
        except Exception as e:
            logging.error(f"❌ Error durante scraping: {e}")
        finally:
            driver.quit()
            logging.info("🚗 Navegador cerrado.")

        logging.info("😴 Pausando por 5 horas antes del próximo intento...\n")
        time.sleep(5 * 60 * 60)  # 5 horas en segundos

if __name__ == "__main__":
    logging.info("🚀 Script de ofertas iniciado por Ohm-Aster.")
    main()
