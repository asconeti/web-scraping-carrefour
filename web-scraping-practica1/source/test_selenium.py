from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# ⚙️ Configura Chrome en mode headless per entorns sense interfície gràfica
options = Options()
# 🧠 Aquí afegim el user-agent
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
options.add_argument('--headless')  # Important: no hi ha interfície gràfica
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# 🧭 Especifica manualment el path al binari de Chromium si cal
options.binary_location = "/usr/bin/chromium"  # Canvia si el binari està en un altre lloc

# 🚀 Llança el navegador amb el driver del sistema (ja instal·lat)
driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)

# 🌐 Obre la pàgina de Carrefour
driver.get("https://www.carrefour.es/supermercado")

# ⏱️ Esperem uns segons per deixar que carregui
time.sleep(5)

# 🖨️ Mostrem el títol per confirmar que s’ha obert correctament
print("Títol de la pàgina:", driver.title)

# ✅ Tanca el navegador
driver.quit()
