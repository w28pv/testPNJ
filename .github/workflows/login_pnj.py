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
    username = os.getenv("PNJ_USERNAME")
    password = os.getenv("PNJ_PASSWORD")

    if not username or not password:
        raise Exception("Missing PNJ_USERNAME or PNJ_PASSWORD")

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

        driver.get("https://example.com/login")

        wait.until(EC.presence_of_element_located((By.ID, "username")))

        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password, Keys.RETURN)

        # Wait until login success
        wait.until(EC.url_contains("dashboard"))

        assert "dashboard" in driver.current_url

        print("✅ Login OK")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
