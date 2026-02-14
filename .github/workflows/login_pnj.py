import os
import sys
import time
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


LOGIN_URL = "https://message.pnj.com.vn/login"
# Sau đăng nhập thành công, portal có thể chuyển về "/" hoặc một dashboard cụ thể.
# Nếu bạn biết URL/selector chắc chắn, cập nhật CHECK_XPATH/CSS bên dưới cho nhanh ổn định.
POST_LOGIN_CHECK_CANDIDATES = [
    # Ưu tiên 1: một phần tử/h1 hiển thị sau đăng nhập (cập nhật theo thực tế)
    (By.CSS_SELECTOR, "header .user-name"),
    (By.XPATH, "//a[contains(@href,'/dang-xuat') or contains(.,'Đăng xuất')]"),
    # Ưu tiên 2: URL đổi khác /login
]

# Các khả năng locator cho input user/pass theo thực tế thường gặp
USERNAME_CANDIDATES = [
    (By.ID, "username"),
    (By.NAME, "username"),
    (By.ID, "email"),
    (By.NAME, "email"),
    (By.CSS_SELECTOR, "input[type='email']"),
    (By.CSS_SELECTOR, "input[placeholder*='email' i]"),
    (By.CSS_SELECTOR, "input[placeholder*='đăng nhập' i]"),
    (By.CSS_SELECTOR, "input[placeholder*='tên người dùng' i]"),
]

PASSWORD_CANDIDATES = [
    (By.ID, "password"),
    (By.NAME, "password"),
    (By.CSS_SELECTOR, "input[type='password']"),
    (By.CSS_SELECTOR, "input[placeholder*='mật khẩu' i]"),
]

SUBMIT_CANDIDATES = [
    (By.CSS_SELECTOR, "button[type='submit']"),
    (By.XPATH, "//button[contains(.,'Đăng nhập') or contains(.,'Login')]"),
    (By.CSS_SELECTOR, "input[type='submit']"),
]


def create_driver(headless: bool = True) -> webdriver.Chrome:
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    # Cài đặt khuyến nghị cho môi trường CI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--lang=vi-VN")
    # Dùng profile tạm để tránh lỗi “user data dir in use” trên CI
    chrome_options.add_argument("--user-data-dir=/tmp/selenium_user_data")
    chrome_options.add_argument("--disable-notifications")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(60)
    return driver


def find_first_present(driver, candidates, timeout=15) -> Optional[webdriver.remote.webelement.WebElement]:
    for by, selector in candidates:
        try:
            return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, selector)))
        except Exception:
            continue
    return None


def find_first_clickable(driver, candidates, timeout=15) -> Optional[webdriver.remote.webelement.WebElement]:
    for by, selector in candidates:
        try:
            return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, selector)))
        except Exception:
            continue
    return None


def wait_post_login(driver, timeout=20) -> bool:
    # Điều kiện 1: URL thay đổi ra khỏi /login
    try:
        WebDriverWait(driver, timeout).until(lambda d: "/login" not in d.current_url)
    except Exception:
        pass

    # Điều kiện 2: Tìm thấy một trong các phần tử xác nhận đăng nhập
    for by, selector in POST_LOGIN_CHECK_CANDIDATES:
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((by, selector)))
            return True
        except Exception:
            continue

    # Nếu URL khác /login thì cũng coi như thành công bước đầu (tùy portal)
    return "/login" not in driver.current_url


def login(username: str, password: str, headless: bool = True) -> int:
    driver = create_driver(headless=headless)
    try:
        driver.get(LOGIN_URL)

        # Đợi form tải
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input, button"))
        )

        # Nếu có SSO/redirect (Azure AD/Workplace...), bạn có thể bắt và xử lý tại đây:
        # Ví dụ: phát hiện nút "Đăng nhập bằng Microsoft" => click, rồi xử lý trang Entra ID.
        # (Bổ sung khi biết cơ chế xác thực thực tế)

        user_input = find_first_present(driver, USERNAME_CANDIDATES, timeout=15)
        if not user_input:
            raise RuntimeError("Không tìm thấy ô nhập Username/Email. Cần cập nhật locator.")

        pass_input = find_first_present(driver, PASSWORD_CANDIDATES, timeout=15)
        if not pass_input:
            raise RuntimeError("Không tìm thấy ô nhập Mật khẩu. Cần cập nhật locator.")

        # Clear & nhập liệu
        user_input.clear()
        user_input.send_keys(username)

        pass_input.clear()
        pass_input.send_keys(password)

        submit_btn = find_first_clickable(driver, SUBMIT_CANDIDATES, timeout=10)
        if not submit_btn:
            # Thử nhấn Enter nếu không có nút submit rõ ràng
            pass_input.submit()
        else:
            submit_btn.click()

        # Chờ trạng thái sau đăng nhập
        if not wait_post_login(driver, timeout=30):
            # Lấy thông báo lỗi nếu có
            err_text = ""
            try:
                err = driver.find_element(By.CSS_SELECTOR, ".error, .validation-summary-errors, .alert-danger")
                err_text = err.text.strip()
            except Exception:
                pass
            raise RuntimeError(f"Đăng nhập có vẻ thất bại. URL: {driver.current_url} ; Lỗi: {err_text}")

        # In thông tin xác nhận để workflow dễ kiểm tra
        print("[OK] Đăng nhập thành công!")
        print("URL hiện tại:", driver.current_url)
        # In 300 ký tự đầu của HTML để debug nhanh (không lộ thông tin nhạy cảm)
        html = driver.page_source
        print("HTML snippet:", html[:300].replace("\n", " "))
        return 0

    except Exception as e:
        print("[FAIL] Lỗi đăng nhập:", e, file=sys.stderr)
        # Lưu screenshot để debug (nếu headless vẫn chụp được)
        try:
            ts = int(time.time())
            path = f"screenshot_fail_{ts}.png"
            driver.save_screenshot(path)
            print(f"Đã lưu screenshot: {path}")
        except Exception:
            pass
        return 1
    finally:
        driver.quit()


if __name__ == "__main__":
    username = os.getenv("PNJ_USERNAME")
    password = os.getenv("PNJ_PASSWORD")
    if not username or not password:
        print("Thiếu biến môi trường PNJ_USERNAME/PNJ_PASSWORD", file=sys.stderr)
        sys.exit(2)

    # Cho phép ép headless=false khi cần debug cục bộ
    headless_flag = os.getenv("HEADLESS", "true").lower() != "false"
    sys.exit(login(username, password, headless=headless_flag))
