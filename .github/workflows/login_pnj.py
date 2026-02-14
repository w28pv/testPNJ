from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager



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

        # USERNAME
        username_input = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[contains(@id,'login')]")
            )
        )

        driver.execute_script("arguments[0].scrollIntoView();", username_input)
        username_input.click()
        username_input.clear()
        username_input.send_keys(username)

        # PASSWORD
        password_input = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[contains(@id,'password')]")
            )
        )

        password_input.click()
        password_input.clear()
        password_input.send_keys(password)

        password_input.send_keys(Keys.RETURN)

        # WAIT REDIRECT
        wait.until(EC.url_contains("dashboard"))

        print("✅ Login OK")
        print(driver.current_url)

    finally:
        driver.quit()
