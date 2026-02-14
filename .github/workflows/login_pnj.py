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
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    wait = WebDriverWait(driver, 20)

    try:
        driver.get("https://message.pnj.com.vn/login")

        # username field
        username_input = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[id$='_login']")
            )
        )

        # password field
        password_input = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[id$='_password']")
            )
        )

        username_input.send_keys(username)
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)

        wait.until(EC.url_contains("dashboard"))

        print("✅ Login OK")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
