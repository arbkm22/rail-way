"""
Test script for Indian Railway Map Visualization

This script tests the visualize_railway_map.py module to ensure it
generates the expected output.
"""

import os
import sys
import tempfile
from pathlib import Path


def test_map_generation():
    """Test that the map generation works correctly"""
    # Import the module
    sys.path.insert(0, os.path.dirname(__file__))
    import visualize_railway_map
    
    print("Testing Indian Railway Map Visualization...")
    
    # Test 1: Check that create_railway_map returns a folium.Map object
    print("\n1. Testing create_railway_map() function...")
    railway_map = visualize_railway_map.create_railway_map()
    
    # Check if it's a folium Map object
    import folium
    assert isinstance(railway_map, folium.Map), "create_railway_map() should return a folium.Map object"
    print("   ✓ Returns folium.Map object")
    
    # Test 2: Verify map is centered on India
    print("\n2. Testing map initialization...")
    assert railway_map.location == [20.5937, 78.9629], "Map should be centered on India"
    print("   ✓ Map centered at [20.5937, 78.9629]")
    
    # Test 3: Verify zoom level
    assert railway_map.options['zoom'] == 5, "Zoom level should be 5"
    print("   ✓ Zoom level is 5")
    
    # Test 4: Save to temporary file and verify
    print("\n3. Testing HTML generation...")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as tmp_file:
        tmp_filename = tmp_file.name
    
    try:
        railway_map.save(tmp_filename)
        assert os.path.exists(tmp_filename), "HTML file should be created"
        print(f"   ✓ HTML file created: {tmp_filename}")
        
        # Verify file content
        with open(tmp_filename, 'r') as f:
            content = f.read()
        
        # Check for required elements - now using CartoDB Voyager tiles for better geographic detail
        assert 'cartocdn.com' in content or 'carto' in content.lower(), "Should use CartoDB tiles for geographic accuracy"
        print("   ✓ Uses CartoDB Voyager tiles (geographically accurate)")
        
        assert 'New Delhi' in content, "Should include New Delhi station"
        assert 'Chhatrapati' in content, "Should include Mumbai station"
        assert 'Howrah' in content, "Should include Kolkata station"
        assert 'Chennai' in content, "Should include Chennai station"
        assert 'Bengaluru' in content, "Should include Bengaluru station"
        print("   ✓ All 5 stations included")
        
        assert content.count('.bindPopup(') == 5, "Should have 5 popups"
        assert content.count('.bindTooltip(') == 5, "Should have 5 tooltips"
        print("   ✓ All markers have popups and tooltips")
        
        assert 'Station' in content, "Tooltips should display 'Station'"
        print("   ✓ Tooltips display 'Station'")
        
    finally:
        # Clean up
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)
    
    print("\n" + "="*50)
    print("✓ ALL TESTS PASSED!")
    print("="*50)
    
    return True


if __name__ == '__main__':
    try:
        success = test_map_generation()
        sys.exit(0 if success else 1)
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
