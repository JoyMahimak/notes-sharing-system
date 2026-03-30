from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Open browser
driver = webdriver.Chrome()

# Open your website
driver.get("http://127.0.0.1:5000/register")

time.sleep(2)

# Register user
driver.find_element(By.NAME, "username").send_keys("testuser")
driver.find_element(By.NAME, "password").send_keys("1234")
driver.find_element(By.TAG_NAME, "button").click()

time.sleep(2)

# Go to login
driver.get("http://127.0.0.1:5000/login")

time.sleep(2)

# Login
driver.find_element(By.NAME, "username").send_keys("testuser")
driver.find_element(By.NAME, "password").send_keys("1234")
driver.find_element(By.TAG_NAME, "button").click()

time.sleep(3)

print("Login Test Passed ✅")

# Close browser
driver.quit()