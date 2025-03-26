import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import json
import os
from datetime import datetime

# Configuración de Google Sheets
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS")

if not CREDENTIALS_JSON:
    raise ValueError("❌ ERROR: La variable de entorno GOOGLE_CREDENTIALS no está configurada.")

credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(CREDENTIALS_JSON), SCOPES)
client = gspread.authorize(credentials)
spreadsheet = client.open("resultados tracking").sheet1

# Lista de productos
products = [
    {"name": "Escritorio Negro en L", "url": "https://articulo.mercadolibre.com.mx/MLM-2008013683-escritorio-en-forma-de-l-con-almacenamiento-reversible-negro-_JM"},
    {"name": "Escritorio en L 5 cajones", "url": "https://articulo.mercadolibre.com.mx/MLM-2215533921-envio-gratis-escritorio-moderno-oficina-en-l-con-5-cajones-_JM"},
]

# Headers y configuración
HEADERS_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

def get_price(url):
    """Obtiene el precio del producto en Mercado Libre."""
    for _ in range(3):  # Reintentar hasta 3 veces
        try:
            headers = {"User-Agent": HEADERS_LIST[_ % len(HEADERS_LIST)]}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            price_element = soup.select_one("span.andes-money-amount__fraction")
            
            if price_element:
                return price_element.text.strip()
        except requests.RequestException as e:
            print(f"⚠️ Error en {url}: {e}")
        time.sleep(5)
    
    return None

def already_tracked(product_name, url):
    """Verifica si el producto ya está registrado."""
    try:
        records = spreadsheet.get_all_records()
        for row in records:
            if row.get("Nombre") == product_name and row.get("URL") == url:
                return True
    except Exception as e:
        print(f"⚠️ No se pudo verificar registros previos: {e}")
    return False

# Procesar cada producto
for product in products:
    print(f"\n🔍 Buscando precio para '{product['name']}'...")
    
    if already_tracked(product["name"], product["url"]):
        print(f"⚠️ '{product['name']}' ya registrado. Saltando...")
        continue

    price = get_price(product["url"])
    
    if price:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"✅ Precio obtenido: {price} MXN")
        spreadsheet.append_row([product["name"], product["url"], price, timestamp])
    else:
        print(f"⚠️ No se encontró precio para '{product['name']}'.")

    time.sleep(5)  # Espera para evitar bloqueos

print("\n✅ Proceso finalizado.")

time.sleep(60)  # Espera para evitar bloqueos
