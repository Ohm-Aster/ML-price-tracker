# 🛍️ ML Price Tracker

Este proyecto es un **scraper automatizado** que extrae productos en oferta desde [Mercado Libre México](https://www.mercadolibre.com.mx/ofertas#nav-header) y guarda los datos directamente en una hoja de cálculo de Google Sheets.

---

## ✨ Características

- Obtiene nombre, precio actual, precio anterior y enlace del producto.
- Registra la fecha y hora de la búsqueda.
- Se ejecuta automáticamente cada 5 horas.
- Guarda los datos en tiempo real en una hoja de cálculo.
- Usable como script local o desplegable en servicios como **Render**.

---

## ⚙️ Tecnologías usadas

- 🐍 Python 3
- 🌐 Selenium (navegación automática)
- 📄 Google Sheets API vía `gspread`
- ☁️ Render (para ejecución automática)
- 🛠️ WebDriver Manager (manejo automático de ChromeDriver)

---

## 🧰 Requisitos

1. Tener Python 3.8 o superior.
2. Tener un archivo `credentials.json` con acceso a la Google Sheet deseada.
3. Crear una hoja de cálculo llamada **"resultados tracking"** y compartirla con el correo del cliente del archivo `credentials.json`.

---

## 🚀 Instalación y uso local

```bash
git clone https://github.com/tu-usuario/ML-price-tracker.git
cd ML-price-tracker
pip install -r requirements.txt
python scraper.py
```

---

## ☁️ Despliegue en Render

1. Crea un nuevo servicio tipo Background Worker.
2. Sube el código o conecta tu repo de GitHub.
3. Asegúrate de incluir el archivo credentials.json en tu raíz del proyecto.
4. Usa este comando como entrada: python scraper.py

---

## 📊 Ejemplo de salida

2025-04-08 12:30:00 - Laptop HP - 12,999 MXN (antes: 14,999) - https://www.mercadolibre.com.mx/...
✅ Datos guardados en Google Sheets exitosamente.

