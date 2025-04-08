import time
import json
import os
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configuración de Google Sheets
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
with open("credentials.json") as f:
    creds_data = json.load(f)
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_data, SCOPES)
client = gspread.authorize(credentials)
sheet = client.open("resultados tracking").sheet1  # Nombre de la hoja

# Configuración del navegador (Selenium)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Para ejecutar sin interfaz gráfica
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# URL de búsqueda en MercadoLibre
search_url = "https://www.mercadolibre.com.mx/ofertas#nav-header"

driver.get(search_url)
time.sleep(3)  # Espera para que la página cargue

productos = []
fecha_busqueda = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Fecha y hora actual

try:
    # Encuentra los elementos de los productos
    items = driver.find_elements(By.CSS_SELECTOR, 'a.poly-component__title')
    precios_actuales = driver.find_elements(By.CSS_SELECTOR, 'div.poly-price__current span.andes-money-amount__fraction')
    precios_anteriores = driver.find_elements(By.CSS_SELECTOR, 's.andes-money-amount--previous span.andes-money-amount__fraction')

    for i in range(len(items)):
        nombre = items[i].text
        url = items[i].get_attribute("href")
        precio_actual = precios_actuales[i].text if i < len(precios_actuales) else "No disponible"
        precio_anterior = precios_anteriores[i].text if i < len(precios_anteriores) else "Sin descuento"

        productos.append([fecha_busqueda, nombre, precio_actual, precio_anterior, url])
        print(f"✅ {fecha_busqueda} - {nombre} - {precio_actual} MXN (antes: {precio_anterior} MXN) - {url}")

    # Guarda los datos en Google Sheets
    if productos:
        sheet.append_rows(productos)
        print("📌 Datos guardados en Google Sheets exitosamente.")

except Exception as e:
    print(f"❌ ERROR al extraer productos: {e}")

finally:
    driver.quit()
