"""
Indian Railway Map Visualization
Displays major railway stations on a realistic map of India using folium
"""

import folium

def create_railway_map():
    """
    Create an interactive map of India with major railway stations plotted.
    Uses OpenStreetMap tiles for realistic rendering.
    """
    
    # Initialize the map centered on India
    india_map = folium.Map(
        location=[20.5937, 78.9629],  # Center of India
        zoom_start=5,
        tiles='OpenStreetMap'
    )
    
    # Define railway station data with exact coordinates
    railway_stations = [
        {
            'name': 'New Delhi (NDLS)',
            'lat': 28.6414,
            'lon': 77.2195
        },
        {
            'name': 'Chhatrapati Shivaji Maharaj Terminus (Mumbai)',
            'lat': 18.9398,
            'lon': 72.8355
        },
        {
            'name': 'Howrah Junction (Kolkata)',
            'lat': 22.5833,
            'lon': 88.3417
        },
        {
            'name': 'MGR Chennai Central',
            'lat': 13.0827,
            'lon': 80.2707
        },
        {
            'name': 'KSR Bengaluru City Junction',
            'lat': 12.9776,
            'lon': 77.5713
        }
    ]
    
    # Plot each station on the map
    for station in railway_stations:
        folium.Marker(
            location=[station['lat'], station['lon']],
            popup=station['name'],
            tooltip='Station'
        ).add_to(india_map)
    
    # Save the map to an HTML file
    india_map.save('india_railways.html')
    print("Map successfully created and saved to 'india_railways.html'")
    print(f"Total stations plotted: {len(railway_stations)}")
    
    return india_map


if __name__ == '__main__':
    create_railway_map()
