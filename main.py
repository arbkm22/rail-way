from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url = "https://www.prokerala.com/travel/indian-railway/trains/"
driver.get(url=url)
print(driver.title)

sleep(5)

driver.quit()