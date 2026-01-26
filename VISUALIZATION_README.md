# Indian Railway Map Visualization

## Overview

This module provides a high-quality, realistic, interactive map visualization of Indian Railway stations using the Folium library with tile-based rendering.

## Features

- **Realistic Map Rendering**: Uses OpenStreetMap tiles for a professional, navigation-map appearance
- **Interactive Markers**: Each railway station is marked with:
  - A clickable popup showing the station name
  - A hover tooltip displaying "Station"
- **Major Railway Stations**: Displays 5 key Indian railway stations with exact coordinates

## Requirements

```bash
pip install folium
```

Or install from requirements.txt:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Script

```bash
python3 visualize_railway_map.py
```

This will generate an HTML file named `india_railways.html` in the current directory.

### Viewing the Map

Open the generated `india_railways.html` file in any modern web browser:

```bash
# On Linux
xdg-open india_railways.html

# On macOS
open india_railways.html

# On Windows
start india_railways.html
```

## Railway Stations Included

The map displays the following major Indian railway stations:

| Station Name | Location | Coordinates |
|--------------|----------|-------------|
| New Delhi (NDLS) | Delhi | 28.6414°N, 77.2195°E |
| Chhatrapati Shivaji Maharaj Terminus | Mumbai | 18.9400°N, 72.8355°E |
| Howrah Junction | Kolkata | 22.5835°N, 88.3426°E |
| MGR Chennai Central | Chennai | 13.0827°N, 80.2753°E |
| KSR Bengaluru City Junction | Bengaluru | 12.9776°N, 77.5718°E |

## Map Configuration

- **Center**: India (20.5937°N, 78.9629°E)
- **Zoom Level**: 5 (shows entire country)
- **Tile Source**: OpenStreetMap (high-quality, realistic map tiles)

## Testing

Run the test suite to verify the map generation:

```bash
python3 test_visualize_railway_map.py
```

## Implementation Details

### Why Folium?

The script uses the Folium library instead of GeoPandas plotting because:

1. **Tile-based Rendering**: Folium uses real map tiles (like Google Maps or OpenStreetMap), not simplified vector shapes
2. **Interactive**: The output is an interactive HTML map that users can zoom and pan
3. **Professional Appearance**: Looks like a standard navigation map with roads, state borders, and labels
4. **No "Low Polygon 2D Game Map"**: Avoids the simplified geometric appearance of vector-based plotting

### Code Structure

The script is organized into two main functions:

- `create_railway_map()`: Creates and configures the Folium map with station markers
- `main()`: Handles script execution and file output

## Customization

To add more stations, edit the `railway_stations` list in `create_railway_map()`:

```python
railway_stations = [
    {
        'name': 'Station Name',
        'latitude': XX.XXXX,
        'longitude': YY.YYYY
    },
    # Add more stations here
]
```

To change the map center or zoom:

```python
india_map = folium.Map(
    location=[latitude, longitude],  # Change center
    zoom_start=5,                    # Adjust zoom level
    tiles='OpenStreetMap'            # Or use other tile providers
)
```

## Output

The script generates a single HTML file (`india_railways.html`) that:
- Is self-contained (includes all necessary JavaScript/CSS via CDN)
- Works offline after initial load (map tiles require internet)
- Can be shared and viewed on any device with a web browser
- Is approximately 8KB in size

## License

This module is part of the Indian Railways Route Finder project and is licensed under the MIT License.
