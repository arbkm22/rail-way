"""
Script to extract timetable data for all trains from prokerala.com
The script visits each train's detail page and extracts the complete timetable
including all stations, arrival/departure times.
"""
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import pandas as pd
import os

def extract_train_timetable(driver, train_number):
    """
    Extract timetable for a specific train
    Returns a list of stations with arrival/departure times
    """
    try:
        url = f"https://www.prokerala.com/travel/indian-railway/trains/{train_number}/"
        driver.get(url)
        
        # Wait for the timetable to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "table")))
        
        # Find the timetable table
        tables = driver.find_elements(By.TAG_NAME, "table")
        
        if not tables:
            print(f"No timetable found for train {train_number}")
            return []
        
        # Extract timetable data
        timetable = []
        for table in tables:
            rows = table.find_elements(By.TAG_NAME, "tr")
            
            for i, row in enumerate(rows):
                if i == 0:  # Skip header
                    continue
                
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 5:
                    station_data = {
                        'station_code': cells[0].text.strip(),
                        'station_name': cells[1].text.strip(),
                        'arrival_time': cells[2].text.strip(),
                        'departure_time': cells[3].text.strip(),
                        'distance_km': cells[4].text.strip() if len(cells) > 4 else ''
                    }
                    timetable.append(station_data)
        
        return timetable
    
    except Exception as e:
        print(f"Error extracting timetable for train {train_number}: {str(e)}")
        return []

def main():
    # Load existing train list
    with open('all_trains.json', 'r') as f:
        trains = json.load(f)
    
    print(f"Total trains to process: {len(trains)}")
    
    # Setup Chrome driver
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Store all timetables
    all_timetables = {}
    
    # Process trains in batches
    batch_size = 100
    
    # Check if we have partial data
    if os.path.exists('train_timetables.json'):
        with open('train_timetables.json', 'r') as f:
            all_timetables = json.load(f)
        print(f"Resuming; {len(all_timetables)} timetables already loaded")
    
    processed_train_numbers = set(all_timetables.keys())
    
    try:
        for i, train in enumerate(trains):
            train_no = train['trainNo']
            # Skip trains that have already been processed
            if str(train_no) in processed_train_numbers:
                continue
            print(f"Processing train {i+1}/{len(trains)}: {train_no} - {train['trainName']}")
            
            timetable = extract_train_timetable(driver, train_no)
            
            if timetable:
                all_timetables[str(train_no)] = {
                    'trainNo': train_no,
                    'trainName': train['trainName'],
                    'fromStation': train['fromStation'],
                    'toStation': train['toStation'],
                    'timetable': timetable
                }
            
            # Save progress every batch_size trains
            if (i + 1) % batch_size == 0:
                with open('train_timetables.json', 'w') as f:
                    json.dump(all_timetables, f, indent=2)
                print(f"Progress saved: {len(all_timetables)} trains processed")
            
            # Be respectful to the server
            sleep(0.5)
    
    except KeyboardInterrupt:
        print("\nInterrupted by user. Saving progress...")
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
    
    finally:
        # Save final data
        with open('train_timetables.json', 'w') as f:
            json.dump(all_timetables, f, indent=2)
        
        print(f"\nTotal timetables extracted: {len(all_timetables)}")
        print("Data saved to train_timetables.json")
        
        driver.quit()

if __name__ == "__main__":
    main()
