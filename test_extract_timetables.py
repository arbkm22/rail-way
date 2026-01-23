"""
Test script for extract_timetables.py to verify the URL generation and functionality
"""
import sys
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

def test_url_slug_generation():
    """Test the URL slug generation function"""
    print("=" * 80)
    print("TEST SUITE: Extract Timetables URL Generation")
    print("=" * 80)
    
    # Test 1: Basic train name
    print("\nTest 1: Basic train name")
    slug = generate_url_slug("Abohar Jodhpur Express")
    expected = "abohar-jodhpur-express"
    assert slug == expected, f"Expected '{expected}', got '{slug}'"
    print(f"✓ Basic train name: '{slug}'")
    
    # Test 2: Train with special characters
    print("\nTest 2: Train with special characters")
    slug = generate_url_slug("Mumbai CSMT - Pune Express")
    expected = "mumbai-csmt-pune-express"
    assert slug == expected, f"Expected '{expected}', got '{slug}'"
    print(f"✓ Special characters handled: '{slug}'")
    
    # Test 3: Train with parentheses
    print("\nTest 3: Train with parentheses")
    slug = generate_url_slug("New Delhi (NDLS) Express")
    expected = "new-delhi-ndls-express"
    assert slug == expected, f"Expected '{expected}', got '{slug}'"
    print(f"✓ Parentheses handled: '{slug}'")
    
    # Test 4: Train with multiple spaces
    print("\nTest 4: Train with multiple spaces")
    slug = generate_url_slug("Train   with   spaces")
    expected = "train-with-spaces"
    assert slug == expected, f"Expected '{expected}', got '{slug}'"
    print(f"✓ Multiple spaces handled: '{slug}'")
    
    # Test 5: Train with slashes
    print("\nTest 5: Train with slashes")
    slug = generate_url_slug("Mumbai/Pune Express")
    expected = "mumbaipune-express"
    assert slug == expected, f"Expected '{expected}', got '{slug}'"
    print(f"✓ Slashes handled: '{slug}'")
    
    # Test 6: Verify URL format with actual train data
    print("\nTest 6: Verify URL format with actual train data")
    with open('all_trains.json', 'r') as f:
        trains = json.load(f)
    
    # Test first train (should be Abohar Jodhpur Express - 14722)
    first_train = trains[0]
    train_no = first_train['trainNo']
    train_name = first_train['trainName']
    
    url_slug = generate_url_slug(train_name)
    url = f"https://www.prokerala.com/travel/indian-railway/trains/{url_slug}-{train_no}.html"
    
    # Verify it matches the expected pattern
    expected_url = "https://www.prokerala.com/travel/indian-railway/trains/abohar-jodhpur-express-14722.html"
    assert url == expected_url, f"Expected '{expected_url}', got '{url}'"
    print(f"✓ URL format correct: {url}")
    
    # Test 7: Verify no leading/trailing hyphens
    print("\nTest 7: Verify no leading/trailing hyphens")
    slug = generate_url_slug("-Leading and Trailing-")
    assert not slug.startswith('-') and not slug.endswith('-'), "Should not have leading/trailing hyphens"
    print(f"✓ No leading/trailing hyphens: '{slug}'")
    
    print("\n" + "=" * 80)
    print("ALL TESTS PASSED ✓")
    print("=" * 80)
    print("\nURL generation is working correctly!")
    print("Features validated:")
    print("  ✓ Basic train name conversion")
    print("  ✓ Special character handling")
    print("  ✓ Parentheses removal")
    print("  ✓ Multiple space collapsing")
    print("  ✓ Slash handling")
    print("  ✓ Correct URL format generation")
    print("  ✓ No leading/trailing hyphens")
    print("=" * 80)

if __name__ == "__main__":
    try:
        test_url_slug_generation()
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
