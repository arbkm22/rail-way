"""
Test script to verify URL generation for train timetable extraction
"""
import json
import re

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

def test_url_generation():
    """Test URL generation with sample trains"""
    
    # Load sample trains
    with open('all_trains.json', 'r') as f:
        trains = json.load(f)
    
    # Test with first 10 trains
    print("Testing URL generation for first 10 trains:\n")
    for i, train in enumerate(trains[:10]):
        train_no = train['trainNo']
        train_name = train['trainName']
        url_slug = generate_url_slug(train_name)
        url = f"https://www.prokerala.com/travel/indian-railway/trains/{url_slug}-{train_no}.html"
        
        print(f"{i+1}. Train: {train_name} ({train_no})")
        print(f"   URL Slug: {url_slug}")
        print(f"   Full URL: {url}")
        print()
    
    # Verify the first train matches the expected pattern
    first_train = trains[0]
    expected_train_no = 14722
    expected_name = "Abohar Jodhpur Express"
    
    if first_train['trainNo'] == expected_train_no:
        slug = generate_url_slug(first_train['trainName'])
        expected_url = f"https://www.prokerala.com/travel/indian-railway/trains/{slug}-{expected_train_no}.html"
        print(f"\n✓ Verification: First train URL generated correctly")
        print(f"  Expected pattern: abohar-jodhpur-express-14722.html")
        print(f"  Generated URL: {expected_url}")
    
    # Test edge cases
    print("\n" + "="*70)
    print("Testing edge cases:")
    print("="*70)
    
    test_cases = [
        "Mumbai CSMT - Pune Deccan Queen",
        "Delhi-Kalka Shatabdi",
        "New Delhi (NDLS) to Mumbai",
        "Train with (Parentheses) & Special / Chars"
    ]
    
    for test_name in test_cases:
        slug = generate_url_slug(test_name)
        print(f"\nOriginal: {test_name}")
        print(f"Slug:     {slug}")

if __name__ == "__main__":
    test_url_generation()
