import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def main():
    username = "kiet.hmt"
    password = "Kiet$123"

    chrome_options = Options()

    # Required for GitHub Actions
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        wait = WebDriverWait(driver, 20)

        driver.get("https://message.pnj.com.vn/login")

        wait.until(EC.presence_of_element_located((By.ID, "_EmployeeLogin_INSTANCE_9WKQN0ib39gl_login")))

        driver.find_element(By.ID, "_EmployeeLogin_INSTANCE_9WKQN0ib39gl_login").send_keys(username)
        driver.find_element(By.ID, "_EmployeeLogin_INSTANCE_9WKQN0ib39gl_password").send_keys(password, Keys.RETURN)

        # Wait until login success
        wait.until(EC.url_contains("dashboard"))

        assert "dashboard" in driver.current_url

        print("✅ Login OK")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
