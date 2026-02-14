from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

driver.get("https://example.com/login")

driver.find_element(By.ID, "username").send_keys("kiet.hmt")
driver.find_element(By.ID, "password").send_keys("Kiet$123", Keys.RETURN)

# Kiểm tra login thành công
wait.until(EC.url_contains("dashboard"))
assert "dashboard" in driver.current_url

print("Login OK")

driver.quit()
