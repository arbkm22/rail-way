# Indian Railways Route Finder

A modern train route finder application for Indian Railways built with Next.js and TypeScript - **no Python backend required!**

## 🚀 Quick Start

**Simple Single-Command Start**

1. Install and start the Next.js application:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

2. Open http://localhost:3000 in your browser

That's it! The application now uses Next.js API routes instead of a separate Python backend, making it much simpler to run and deploy.

---

## Features

- **Modern Web Interface**: Next.js with interactive Leaflet maps
- **Serverless Architecture**: Next.js API routes - no separate backend server needed!
- **TypeScript**: Fully type-safe route finding algorithm
- **Direct Route Finding**: Find all direct trains between two stations
- **Multi-hop Route Search**: Intelligently find routes requiring train changes
- **Timing Constraints**: Ensures waiting time at intermediate stations doesn't exceed 4 hours
- **Interactive Maps**: Visualize routes on OpenStreetMap with color-coded markers
- **Mobile Responsive**: Works on all devices
- **No Paid Services**: Uses free OpenStreetMap tiles
- **Easy Deployment**: Deploy to Vercel, Netlify, or any Next.js hosting platform

## Architecture

### Current Stack
- **Frontend**: Next.js 16 (App Router) + TypeScript + Tailwind CSS
- **Backend**: Next.js API Routes (serverless functions)
- **Route Finding**: TypeScript algorithm (ported from Python)
- **Map**: Leaflet.js with OpenStreetMap tiles
- **Data Format**: GeoJSON for routes and stations
- **Data Storage**: Static JSON file bundled with the app

## Project Structure

```
rail-way/
├── frontend/                       # Next.js application
│   ├── app/                       # App Router
│   │   ├── api/                  # API routes (serverless functions)
│   │   │   ├── stations/        # GET /api/stations
│   │   │   └── routes/find/     # POST /api/routes/find
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/                # React components
│   │   └── Map.tsx
│   ├── lib/                       # Core logic
│   │   ├── routeFinder.ts        # Route finding algorithm (TypeScript)
│   │   └── api.ts                # API client
│   ├── public/
│   │   └── train_timetables.json # Train schedule data
│   └── package.json
├── legacy/                         # Legacy Python files (for reference)
│   ├── api.py                     # Old Flask API
│   ├── app.py                     # Old Flask web app
│   ├── route_finder.py            # Original Python algorithm
│   └── requirements.txt           # Python dependencies
└── README.md
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/arbkm22/rail-way.git
cd rail-way
```

2. Install dependencies and start the application:
```bash
cd frontend
npm install
npm run dev
```

3. Open http://localhost:3000 in your browser

## Deployment

Deploy to Vercel (recommended for Next.js):

```bash
cd frontend
vercel deploy
```

Or deploy to any other Next.js-compatible hosting platform like Netlify, Cloudflare Pages, or AWS Amplify.

## Usage

### Web Application

Start the development server:
```bash
cd frontend
npm run dev
```

Then open http://localhost:3000

The web interface provides:
- Easy-to-use dropdown menus for station selection
- Advanced options for customizing search parameters
- Beautiful visual display of route results with interactive maps
- Support for both direct and multi-hop routes

### API Routes

The application exposes the following API endpoints:

#### GET /api/stations
Returns a GeoJSON FeatureCollection of all available stations with coordinates.

#### POST /api/routes/find
Find routes between two stations.

Request body:
```json
{
  "from_station": "Mumbai CSMT",
  "to_station": "Pune Junction",
  "max_waiting_hours": 4,
  "max_hops": 3
}
```

Response:
```json
{
  "from_station": "Mumbai CSMT",
  "to_station": "Pune Junction",
  "routes": [
    {
      "route_type": "direct",
      "total_duration": "3h 15m",
      "num_changes": 0,
      "segments": [...],
      "geometry": {...}
    }
  ]
}
```

### Command-Line Interface (Legacy)

> **Note**: The Python CLI is now legacy. The web application is the recommended way to use this tool.

If you want to use the legacy Python CLI:

Run the route finder application (either of these commands works):

```bash
python3 main.py
# or
python3 route_finder.py
```

The CLI application will:
1. Display a list of available stations
2. Ask for your starting station (enter name or number)
3. Ask for your destination station (enter name or number)
4. Display all possible routes sorted by total journey time

#### Example Usage

```
INDIAN RAILWAYS ROUTE FINDER
================================================================================

Available stations (32):
1. Ahmadnagar
2. Akola Junction
...
27. Pune Junction
...
30. Ranchi Junction
...

Enter starting station (or number): 27
Enter destination station (or number): 30

Searching for routes from 'Pune Junction' to 'Ranchi Junction'...
Found 14 route(s):

OPTION 1
================================================================================
Route Type: DIRECT
Total Journey Time: 9h 0m
Number of Changes: 0
================================================================================

Segment 1:
  Train: Pune Hatia SF Express (12875)
  From: Pune Junction
  Departure: 20:30
  To: Ranchi Junction
  Arrival: 05:30
  Duration: 9h 0m
```

### Extracting Timetable Data

#### Option 1: Use Sample Data (for testing)

Generate sample timetable data:
```bash
python3 generate_sample_timetables.py
```

This creates `train_timetables.json` with realistic sample data for testing the route finder.

#### Option 2: Extract Real Data from Website

Extract timetables for all trains from prokerala.com:
```bash
python3 extract_timetables.py
```

**Note**: This script will take several hours to complete as it needs to scrape data for 7000+ trains. The script:
- Saves progress every 100 trains
- Can be resumed if interrupted
- Respects the server with delays between requests

## How It Works

### Route Finding Algorithm

The application uses a modified Breadth-First Search (BFS) algorithm:

1. **Station Graph Construction**: Builds a network of stations and trains from timetable data
2. **Direct Route Search**: First checks for direct trains between source and destination
3. **Multi-hop Search**: If needed, explores routes with train changes using BFS
4. **Timing Validation**: Ensures:
   - Trains arrive at stations before departure
   - Waiting time at intermediate stations ≤ 4 hours (configurable)
   - No circular routes (doesn't revisit stations)
5. **Result Ranking**: Sorts routes by total journey time

### Key Components

#### TrainRouteFinder Class

Main class implementing the route-finding logic:

- `find_direct_trains()`: Finds all direct trains between two stations
- `find_connecting_routes()`: Finds multi-hop routes with connections
- `find_all_routes()`: Combines direct and connecting routes
- `print_route()`: Pretty-prints route information

#### Time Handling

The system:
- Parses time strings (HH:MM format)
- Handles day crossovers (e.g., departing 23:00, arriving 02:00 next day)
- Calculates waiting times and journey durations
- Validates timing constraints

## Configuration

You can modify the following parameters in `route_finder.py`:

```python
# In find_all_routes() call
max_waiting_hours=4  # Maximum waiting time at intermediate stations
max_hops=3           # Maximum number of train changes
```

## Data Format

### Train Timetable JSON Structure

```json
{
  "12875": {
    "trainNo": 12875,
    "trainName": "Pune Hatia SF Express",
    "fromStation": "Pune Junction",
    "toStation": "Hatia",
    "timetable": [
      {
        "station_code": "PUNE",
        "station_name": "Pune Junction",
        "arrival_time": "Source",
        "departure_time": "20:30",
        "distance_km": "0"
      },
      {
        "station_code": "NGP",
        "station_name": "Nagpur Junction",
        "arrival_time": "10:30",
        "departure_time": "10:45",
        "distance_km": "718"
      }
      ...
    ]
  }
}
```

## Example Queries

### Direct Train
```
From: Pune Junction
To: Ranchi Junction
Result: Pune Hatia SF Express (direct, 9h journey)
```

### Multi-hop Route
```
From: Pune Junction
To: Howrah Junction
Route 1: Pune → Nagpur (Pune Nagpur Express)
         Nagpur → Howrah (Nagpur Howrah Duronto)
Total Time: ~20h with 3h 30m waiting at Nagpur
```

## Limitations

- Currently uses sample data with limited trains (for testing)
- Time calculations assume trains run daily
- Does not account for:
  - Train cancellations
  - Delays
  - Days of operation
  - Seat availability
  - Fare information

## Future Enhancements

- [x] Web-based UI
- [ ] Extract complete timetable data for all 7000+ trains
- [ ] Add train running days (Mon-Sun schedule)
- [ ] Include fare calculation
- [ ] Real-time train status integration
- [ ] Platform information
- [ ] Coach composition details
- [ ] Seat availability checking
- [ ] Save favorite routes
- [ ] Export routes to PDF/calendar

## Contributing

Contributions are welcome! Areas for improvement:
- Data extraction optimization
- Algorithm efficiency
- Additional features
- UI/UX improvements
- Documentation

## License

MIT License

## Acknowledgments

- Train data sourced from [ProKerala](https://www.prokerala.com/travel/indian-railway/trains/)
- Inspired by the need for multi-hop train route planning in India

## Contact

For issues, questions, or suggestions, please open an issue on GitHub.
