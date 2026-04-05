from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

driver.get("http://127.0.0.1:5000")

wait = WebDriverWait(driver, 10)

try:
    username = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    password = driver.find_element(By.NAME, "password")

    username.send_keys("admin")
    password.send_keys("admin@123")

    driver.find_element(By.TAG_NAME, "button").click()

    print("✅ Selenium Test Passed")

except Exception as e:
    print("❌ Selenium Test Failed:", e)

driver.quit()