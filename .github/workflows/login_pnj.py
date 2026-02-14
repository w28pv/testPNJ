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

# Mở trình duyệt Chrome (Selenium 4 tự nhận driver nếu đã cài Chrome mới)
driver = webdriver.Chrome()

# Vào trang web
driver.get("https://message.pnj.com.vn/login")

# Chờ 2 giây cho trang load (cách đơn giản)
time.sleep(5)

# Tìm ô nhập bằng ID
username = driver.find_element(By.ID, "_EmployeeLogin_INSTANCE_9WKQN0ib39gl_login")
password = driver.find_element(By.ID, "_EmployeeLogin_INSTANCE_9WKQN0ib39gl_password")

# Nhập dữ liệu
username.send_keys("kiet.hmt")
password.send_keys("Kiet$123")

# Nhấn Enter để đăng nhập
password.send_keys(Keys.RETURN)

# Hoặc nếu có nút login ID là "loginBtn"
# driver.find_element(By.ID, "loginBtn").click()

# Chờ xem kết quả
time.sleep(5)

# Đóng trình duyệt
driver.quit()
