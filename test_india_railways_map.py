"""
Test script for india_railways_map.py
"""
import os
import sys

def test_railway_map_generation():
    """Test that the railway map script generates the expected output."""
    
    # Import the module
    from india_railways_map import create_railway_map
    
    # Remove existing output file if present
    output_file = 'india_railways.html'
    if os.path.exists(output_file):
        os.remove(output_file)
    
    # Generate the map
    print("Testing map generation...")
    map_obj = create_railway_map()
    
    # Verify output file was created
    assert os.path.exists(output_file), "HTML file was not created"
    print("✓ HTML file created successfully")
    
    # Verify file has content
    file_size = os.path.getsize(output_file)
    assert file_size > 1000, f"HTML file is too small ({file_size} bytes)"
    print(f"✓ HTML file has content ({file_size} bytes)")
    
    # Read and verify content
    with open(output_file, 'r') as f:
        content = f.read()
    
    # Check for required elements
    required_elements = [
        'openstreetmap.org',  # OpenStreetMap tiles
        '20.5937',  # India center latitude
        '78.9629',  # India center longitude
        '"zoom": 5',  # Zoom level
        'New Delhi (NDLS)',
        'Chhatrapati Shivaji Maharaj Terminus (Mumbai)',
        'Howrah Junction (Kolkata)',
        'MGR Chennai Central',
        'KSR Bengaluru City Junction',
    ]
    
    for element in required_elements:
        assert element in content, f"Missing required element: {element}"
        print(f"✓ Found: {element}")
    
    # Count markers (should be 5)
    marker_count = content.count('L.marker')
    assert marker_count == 5, f"Expected 5 markers, found {marker_count}"
    print(f"✓ Found {marker_count} markers")
    
    # Count Station tooltips (should be 5)
    station_count = content.count('Station')
    assert station_count >= 5, f"Expected at least 5 'Station' tooltips, found {station_count}"
    print(f"✓ Found {station_count} 'Station' references")
    
    print("\n✅ All tests passed!")
    return True


if __name__ == '__main__':
    try:
        test_railway_map_generation()
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
