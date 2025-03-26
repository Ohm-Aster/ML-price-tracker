import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import json
import os

# Configuración de la API de Google Sheets
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# validar existencia
#CREDENTIALS_FILE = "credentials.json"  
CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS")

SPREADSHEET_NAME = "resultados tracking"

# Autenticación con Google Sheets
#credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPES)
credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(CREDENTIALS_JSON), SCOPES)
client = gspread.authorize(credentials)
spreadsheet = client.open(SPREADSHEET_NAME).sheet1

# Lista de productos en Mercado Libre (URLS)
products = [
    {"name": "Escritorio Negro en L", "url": "https://articulo.mercadolibre.com.mx/MLM-2008013683-escritorio-en-forma-de-l-con-almacenamiento-reversible-negro-_JM"},
    {"name": "Escritorio en L 5 cajones", "url": "https://articulo.mercadolibre.com.mx/MLM-2215533921-envio-gratis-escritorio-moderno-oficina-en-l-con-5-cajones-_JM"},
]

# Headers para evitar bloqueos
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def get_price(url):
    """Obtiene el precio del producto en Mercado Libre"""
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"❌ Error al acceder a {url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Intentar obtener el precio con diferentes clases
    price_element = soup.select_one("span.andes-money-amount__fraction")
    if not price_element:
        print(f"❌ No se pudo obtener el precio en {url}")
        return None

    return price_element.text.strip()

# Recorrer cada producto y actualizar en Google Sheets
for product in products:
    print(f"🔍 Buscando precio para {product['name']}...")
    price = get_price(product["url"])
    
    if price:
        print(f"✅ Precio obtenido: {price} MXN")
        spreadsheet.append_row([product["name"], product["url"], price])
    else:
        print(f"⚠️ No se encontró precio para {product['name']}")

    time.sleep(5)  # Espera para evitar bloqueos

print("✅ Proceso finalizado. Revisa tu Google Sheet.")
