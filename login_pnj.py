import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = "https://message.pnj.com.vn/login"

USERNAME = "kiet.hmt"
PASSWORD = "Kiet$123"


def main():
    print("Starting PNJ login test...")

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        print("Opening website...")
        driver.get(URL)

        wait = WebDriverWait(driver, 20)

        print("Waiting for username input...")
        username_input = wait.until(
            EC.presence_of_element_located(
                (By.ID, "_EmployeeLogin_INSTANCE_9WKQN0ib39gl_login")
            )
        )

        print("Waiting for password input...")
        password_input = driver.find_element(
            By.ID, "_EmployeeLogin_INSTANCE_9WKQN0ib39gl_password"
        )

        print("Entering credentials...")
        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)

        print("Submitting form...")
        password_input.submit()

        time.sleep(5)

        print("Current URL:", driver.current_url)
        print("Page title:", driver.title)

        # save screenshot for debug
        driver.save_screenshot("pnj_result.png")
        print("Screenshot saved: pnj_result.png")

        print("TEST COMPLETED")

    except Exception as e:
        print("ERROR:", str(e))
        driver.save_screenshot("pnj_error.png")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
