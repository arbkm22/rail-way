# Indian Railway Map Visualization

This script creates a realistic, interactive map of India with major railway stations plotted using the `folium` library and OpenStreetMap tiles.

## Requirements

Install the required dependencies:

```bash
pip install folium
```

Or install all project dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script to generate the map:

```bash
python3 india_railways_map.py
```

This will create an HTML file named `india_railways.html` in the current directory.

## Output

The script generates a high-quality, interactive map featuring:

- **Base Map**: OpenStreetMap tiles providing realistic rendering with roads, state borders, and text labels
- **Center**: India (Latitude: 20.5937, Longitude: 78.9629)
- **Zoom Level**: 5 (shows entire India with good detail)
- **Railway Stations**: 5 major stations plotted with exact coordinates:
  1. New Delhi (NDLS) - 28.6414°N, 77.2195°E
  2. Chhatrapati Shivaji Maharaj Terminus (Mumbai) - 18.9398°N, 72.8355°E
  3. Howrah Junction (Kolkata) - 22.5833°N, 88.3417°E
  4. MGR Chennai Central - 13.0827°N, 80.2707°E
  5. KSR Bengaluru City Junction - 12.9776°N, 77.5713°E

## Features

- **Interactive Map**: Pan, zoom, and explore the map
- **Station Markers**: Each station has a marker with:
  - **Popup**: Click to see the full station name
  - **Tooltip**: Hover to see "Station" label
- **Realistic Rendering**: Unlike simplified vector shapes, this uses tile-based rendering for high-quality, detailed maps

## Opening the Map

Open `india_railways.html` in any web browser to view the interactive map.

## Testing

Run the test suite to verify the map generation:

```bash
python3 test_india_railways_map.py
```

The test validates:
- HTML file creation
- Correct map center coordinates
- Correct zoom level
- OpenStreetMap tile usage
- All 5 railway stations present
- Proper markers and tooltips

## Technical Details

- **Library**: `folium` (Python wrapper for Leaflet.js)
- **Tile Source**: OpenStreetMap
- **Map Projection**: EPSG:3857 (Web Mercator)
- **Output Format**: Self-contained HTML file with embedded JavaScript

## Why Folium?

This implementation uses `folium` with tile-based rendering instead of `geopandas.plot()` because:
1. **Realistic Appearance**: Tile-based maps look like Google Maps or OpenStreetMap with roads, labels, and terrain
2. **Detail**: High-resolution tiles provide much more geographic detail
3. **Interactivity**: Users can zoom and pan to explore the map
4. **No Vector Processing**: Avoids the "low polygon 2D game map" look from simplified vector shapes

## Customization

You can modify the script to:
- Add more railway stations to the `railway_stations` list
- Change the map center or zoom level
- Use different tile providers (e.g., 'Stamen Terrain', 'CartoDB positron')
- Customize marker styles, icons, or colors
- Add additional map features (lines, polygons, etc.)
