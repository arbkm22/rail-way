"""
Demo script to show the improvements in extract_timetables.py

This script demonstrates:
1. The correct URL format generation
2. How threading improves performance (simulated)
"""

import json
import re
from datetime import datetime

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

def main():
    print("=" * 80)
    print("TRAIN TIMETABLE EXTRACTION - IMPROVEMENTS DEMO")
    print("=" * 80)
    
    # Load train data
    with open('all_trains.json', 'r') as f:
        trains = json.load(f)
    
    print(f"\nTotal trains in database: {len(trains)}")
    
    # Show the URL format improvement
    print("\n" + "-" * 80)
    print("IMPROVEMENT 1: Correct URL Format")
    print("-" * 80)
    
    sample_trains = trains[:5]
    
    print("\nOLD URL Format (BROKEN):")
    print("  Pattern: https://www.prokerala.com/travel/indian-railway/trains/{train_number}/")
    for train in sample_trains[:2]:
        old_url = f"https://www.prokerala.com/travel/indian-railway/trains/{train['trainNo']}/"
        print(f"  - {old_url}")
    
    print("\nNEW URL Format (WORKING):")
    print("  Pattern: https://www.prokerala.com/travel/indian-railway/trains/{train-name-slug}-{train_number}.html")
    for train in sample_trains[:2]:
        slug = generate_url_slug(train['trainName'])
        new_url = f"https://www.prokerala.com/travel/indian-railway/trains/{slug}-{train['trainNo']}.html"
        print(f"  - {new_url}")
    
    # Show threading improvement
    print("\n" + "-" * 80)
    print("IMPROVEMENT 2: Parallel Processing with Threading")
    print("-" * 80)
    
    # Calculate estimated time improvement
    avg_time_per_train = 1.0  # seconds (0.5s delay + 0.5s processing)
    total_trains = len(trains)
    
    # Old sequential approach
    sequential_time = total_trains * avg_time_per_train
    sequential_hours = sequential_time / 3600
    
    # New parallel approach (4 threads)
    num_threads = 4
    parallel_time = total_trains * avg_time_per_train / num_threads
    parallel_hours = parallel_time / 3600
    
    improvement_factor = sequential_time / parallel_time
    time_saved_hours = sequential_hours - parallel_hours
    
    print(f"\nConfiguration:")
    print(f"  - Number of parallel threads: {num_threads}")
    print(f"  - Batch size per thread: 25 trains")
    print(f"  - Save interval: Every 100 trains")
    
    print(f"\nEstimated Processing Time:")
    print(f"  OLD (Sequential):  ~{sequential_hours:.1f} hours ({sequential_time/60:.0f} minutes)")
    print(f"  NEW (Parallel):    ~{parallel_hours:.1f} hours ({parallel_time/60:.0f} minutes)")
    print(f"  Time Saved:        ~{time_saved_hours:.1f} hours ({time_saved_hours*60:.0f} minutes)")
    print(f"  Speed Improvement: {improvement_factor:.1f}x faster")
    
    # Show example URLs for verification
    print("\n" + "-" * 80)
    print("SAMPLE URLs for Manual Verification")
    print("-" * 80)
    
    print("\nYou can test these URLs in a browser to verify they work:\n")
    for i, train in enumerate(sample_trains, 1):
        slug = generate_url_slug(train['trainName'])
        url = f"https://www.prokerala.com/travel/indian-railway/trains/{slug}-{train['trainNo']}.html"
        print(f"{i}. {train['trainName']} ({train['trainNo']})")
        print(f"   {url}\n")
    
    # Show key features
    print("-" * 80)
    print("KEY FEATURES")
    print("-" * 80)
    print("\n✓ Fixed URL pattern to match website structure")
    print("✓ Smart URL slug generation from train names")
    print("✓ Parallel processing with 4 threads for 4x speed improvement")
    print("✓ Thread-safe data updates with locking mechanism")
    print("✓ Progress saving every 100 trains (prevents data loss)")
    print("✓ Resume capability (skips already processed trains)")
    print("✓ Graceful error handling for individual train failures")
    print("✓ Respectful server delays (0.3s between requests)")
    
    print("\n" + "=" * 80)
    print("To run the actual extraction:")
    print("  python3 extract_timetables.py")
    print("\nNote: Requires selenium and webdriver_manager packages")
    print("  pip install selenium webdriver-manager")
    print("=" * 80)

if __name__ == "__main__":
    main()
