from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

driver.get("http://localhost:5000")

time.sleep(2)

# Check page title
print("Title:", driver.title)

# Check upload button exists
upload_btn = driver.find_element(By.LINK_TEXT, "Upload")
print("Upload button found")

driver.quit()