from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# 🧠 Configura opcions de Chrome
options = Options()
options.add_argument("--headless")  # Si no vols veure el navegador (treball en contenidors)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# 🔒 Afegim un User-Agent per simular un navegador real
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)

# 🧭 Path manual al driver (canvia si el tens en un altre lloc)
service = Service("/usr/bin/chromedriver")

# 🚀 Iniciem el navegador
driver = webdriver.Chrome(service=service, options=options)

# 🌐 Visitem la web
url = "https://www.carrefour.es/supermercado"
driver.get(url)

# ⏱️ Esperem que carregui completament
time.sleep(5)

# 🖨️ Mostrem el títol per comprovar l'accés
print("Títol de la pàgina:", driver.title)

# ✅ Tanquem el navegador
driver.quit()
