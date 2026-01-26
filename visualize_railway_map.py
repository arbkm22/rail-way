"""
Indian Railway Map Visualization Script

This script creates a high-quality, realistic, interactive map of India
and plots specific real-world Indian Railway Station locations on it using
the folium library with tile-based rendering.
"""

import folium


def create_railway_map():
    """
    Create an interactive map of India with major railway stations plotted.
    
    Returns:
        folium.Map: The generated map object
    """
    # Step 1: Initialize the map centered on India
    # Coordinates: 20.5937, 78.9629 (center of India)
    # Zoom level: 5 (to show entire country)
    india_map = folium.Map(
        location=[20.5937, 78.9629],
        zoom_start=5,
        tiles='OpenStreetMap'
    )
    
    # Step 2: Define the dataset with exact coordinates for railway stations
    railway_stations = [
        {
            'name': 'New Delhi (NDLS)',
            'latitude': 28.6414,
            'longitude': 77.2195
        },
        {
            'name': 'Chhatrapati Shivaji Maharaj Terminus (Mumbai)',
            'latitude': 18.9400,
            'longitude': 72.8355
        },
        {
            'name': 'Howrah Junction (Kolkata)',
            'latitude': 22.5835,
            'longitude': 88.3426
        },
        {
            'name': 'MGR Chennai Central',
            'latitude': 13.0827,
            'longitude': 80.2753
        },
        {
            'name': 'KSR Bengaluru City Junction',
            'latitude': 12.9776,
            'longitude': 77.5718
        }
    ]
    
    # Step 3: Plot the locations with markers
    for station in railway_stations:
        folium.Marker(
            location=[station['latitude'], station['longitude']],
            popup=station['name'],
            tooltip='Station'
        ).add_to(india_map)
    
    return india_map


def main():
    """
    Main function to create and save the railway map.
    """
    # Create the map
    railway_map = create_railway_map()
    
    # Step 4: Save the map to an HTML file
    output_file = 'india_railways.html'
    railway_map.save(output_file)
    
    print(f"✓ Map successfully created and saved to '{output_file}'")
    print(f"✓ Open the file in your web browser to view the interactive map")


if __name__ == '__main__':
    main()
