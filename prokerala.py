from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    url = "https://www.prokerala.com/travel/indian-railway/trains/#alpha-B"
    driver.get(url=url)
    
    # Wait explicitly for table to be present
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    tables = driver.find_elements(By.TAG_NAME, "table")
    print(f"tables: {len(tables)}")

    all_train_data = []
    
    for table_index, table in enumerate(tables):
        headers = [th.text for th in table.find_elements(By.TAG_NAME, "th")]
        for row in table.find_elements(By.TAG_NAME, "tr")[1:]:
            row_data = [td.text for td in row.find_elements(By.TAG_NAME, "td")]
            if row_data:
                all_train_data.append(row_data)
        print(f"Processed table: {table_index + 1}")
    
    df = pd.DataFrame(all_train_data)
    print(f"Total rows collected: {len(all_train_data)}")

    df.to_csv("all_trains.csv", index=False)
    print("Data saved to csv file")

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    driver.quit()