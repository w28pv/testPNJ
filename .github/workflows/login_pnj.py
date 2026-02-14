from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

options = Options()
options.add_argument("--headless=new")   # bắt buộc
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

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
