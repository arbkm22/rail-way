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
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

def generate_url_slug(train_name):
    """
    Convert train name to URL slug format
    Example: "Abohar Jodhpur Express" -> "abohar-jodhpur-express"
    """
    # Convert to lowercase
    slug = train_name.lower()
    # Replace spaces and special characters with hyphens
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    return slug

def extract_train_timetable(driver, train_number, train_name):
    """
    Extract timetable for a specific train
    Returns a list of stations with arrival/departure times
    """
    try:
        # Generate URL with the correct format: {train-name-slug}-{train_number}.html
        url_slug = generate_url_slug(train_name)
        url = f"https://www.prokerala.com/travel/indian-railway/trains/{url_slug}-{train_number}.html"
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

# Thread-safe lock for updating shared data
timetables_lock = threading.Lock()

def process_train_batch(trains_batch, processed_train_numbers):
    """
    Process a batch of trains in a single thread with its own driver
    """
    # Setup Chrome driver for this thread
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    batch_results = {}
    
    try:
        for train in trains_batch:
            train_no = train['trainNo']
            train_name = train['trainName']
            
            # Skip trains that have already been processed
            if str(train_no) in processed_train_numbers:
                continue
            
            print(f"Processing train: {train_no} - {train_name}")
            
            timetable = extract_train_timetable(driver, train_no, train_name)
            
            if timetable:
                batch_results[str(train_no)] = {
                    'trainNo': train_no,
                    'trainName': train_name,
                    'fromStation': train['fromStation'],
                    'toStation': train['toStation'],
                    'timetable': timetable
                }
            
            # Be respectful to the server
            sleep(0.3)
    
    finally:
        driver.quit()
    
    return batch_results

def main():
    # Load existing train list
    with open('all_trains.json', 'r') as f:
        trains = json.load(f)
    
    print(f"Total trains to process: {len(trains)}")
    
    # Store all timetables
    all_timetables = {}
    
    # Check if we have partial data
    if os.path.exists('train_timetables.json'):
        with open('train_timetables.json', 'r') as f:
            all_timetables = json.load(f)
        print(f"Resuming; {len(all_timetables)} timetables already loaded")
    
    processed_train_numbers = set(all_timetables.keys())
    
    # Filter out already processed trains
    trains_to_process = [t for t in trains if str(t['trainNo']) not in processed_train_numbers]
    print(f"Trains remaining to process: {len(trains_to_process)}")
    
    # Configure threading
    num_threads = 4  # Number of parallel threads
    batch_size = 25  # Trains per batch for each thread
    save_interval = 100  # Save progress every N trains
    
    # Create a thread-safe copy of processed train numbers for checking
    processed_train_numbers_frozen = frozenset(processed_train_numbers)
    
    try:
        # Split trains into batches
        batches = [trains_to_process[i:i + batch_size] for i in range(0, len(trains_to_process), batch_size)]
        
        processed_count = len(all_timetables)
        last_save_count = processed_count
        
        # Process batches using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Submit batches to the executor
            future_to_batch = {executor.submit(process_train_batch, batch, processed_train_numbers_frozen): batch for batch in batches}
            
            for future in as_completed(future_to_batch):
                batch = future_to_batch[future]
                try:
                    batch_results = future.result()
                    
                    # Thread-safe update of all_timetables
                    with timetables_lock:
                        all_timetables.update(batch_results)
                        processed_count += len(batch_results)
                        
                        # Save progress periodically
                        if processed_count - last_save_count >= save_interval:
                            with open('train_timetables.json', 'w') as f:
                                json.dump(all_timetables, f, indent=2)
                            print(f"Progress saved: {len(all_timetables)} trains processed")
                            last_save_count = processed_count
                
                except Exception as e:
                    print(f"Error processing batch: {str(e)}")
    
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

if __name__ == "__main__":
    main()
