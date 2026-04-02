from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Start browser
driver = webdriver.Chrome()

# Open website
driver.get("http://127.0.0.1:5000")

# WAIT until username field is visible (THIS FIXES ERROR)
wait = WebDriverWait(driver, 10)

username = wait.until(EC.presence_of_element_located((By.NAME, "username")))
password = driver.find_element(By.NAME, "password")

# Enter data
username.send_keys("admin")
password.send_keys("admin@123")

# Click login
driver.find_element(By.TAG_NAME, "button").click()

print("✅ Selenium Test Passed")

driver.quit()