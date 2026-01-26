# Indian Railways Route Finder - Modern Architecture

A modern train route finder application for Indian Railways with:
- **Backend**: Flask REST API with GeoJSON support
- **Frontend**: Next.js 14 with interactive Leaflet maps
- **Features**: Multi-hop route planning, real-time visualization, mobile-responsive design

## 🏗️ Architecture

### Backend (Flask API)
- Pure REST API (no HTML rendering)
- GeoJSON format for routes and stations
- CORS enabled for frontend communication
- Efficient route-finding algorithm

### Frontend (Next.js)
- App Router architecture
- React with TypeScript
- Leaflet.js for interactive maps
- OpenStreetMap tiles (no paid services)
- Dynamic imports to avoid SSR issues
- Mobile-friendly responsive design

## 📁 Project Structure

```
rail-way/
├── api.py                          # Flask REST API backend
├── route_finder.py                 # Route finding algorithm
├── train_timetables.json          # Train schedule data
├── requirements.txt               # Python dependencies
├── frontend/                      # Next.js application
│   ├── app/                      # App Router pages
│   │   ├── page.tsx             # Main page
│   │   └── layout.tsx           # Root layout
│   ├── components/              # React components
│   │   └── Map.tsx             # Leaflet map component
│   ├── lib/                    # Utilities
│   │   └── api.ts             # API client
│   └── package.json           # Node dependencies
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### 1. Generate Sample Data (First Time Only)

```bash
python3 generate_sample_timetables.py
```

This creates `train_timetables.json` with sample train schedules.

### 2. Start the Flask API Backend

```bash
# Install Python dependencies
pip install -r requirements.txt

# Start Flask API on port 5001
python3 api.py
```

The API will be available at `http://localhost:5001`

### 3. Start the Next.js Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 4. Open in Browser

Navigate to `http://localhost:3000` and start planning routes!

## 🔌 API Endpoints

### GET /api/health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "data_loaded": true
}
```

### GET /api/trains
Get list of all trains.

**Response:**
```json
{
  "trains": [
    {
      "train_no": "12127",
      "train_name": "Mumbai Pune Intercity",
      "from_station": "Mumbai CSMT",
      "to_station": "Pune Junction",
      "num_stops": 4
    }
  ],
  "count": 8
}
```

### GET /api/stations
Get all stations as GeoJSON FeatureCollection.

**Query Parameters:**
- `train_id` (optional): Filter stations for specific train

**Response:**
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [72.8355, 18.9398]
      },
      "properties": {
        "station_name": "Mumbai CSMT",
        "has_coordinates": true
      }
    }
  ]
}
```

### GET /api/trains/{train_id}/route
Get train route as GeoJSON LineString.

**Response:**
```json
{
  "type": "Feature",
  "geometry": {
    "type": "LineString",
    "coordinates": [[72.8355, 18.9398], [73.8742, 18.5284]]
  },
  "properties": {
    "train_no": "12127",
    "train_name": "Mumbai Pune Intercity",
    "stations": [...]
  }
}
```

### POST /api/routes/find
Find routes between two stations.

**Request Body:**
```json
{
  "from_station": "Mumbai CSMT",
  "to_station": "Pune Junction",
  "max_waiting_hours": 4,
  "max_hops": 3
}
```

**Response:**
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
      "geometry": {
        "type": "Feature",
        "geometry": {
          "type": "LineString",
          "coordinates": [...]
        }
      }
    }
  ],
  "count": 1
}
```

## 🎨 Features

### Route Planning
- **Direct Routes**: Find all direct trains between stations
- **Multi-hop Routes**: Intelligent connection finding with timing constraints
- **Flexible Options**: Configure max waiting time and train changes
- **Sorted Results**: Routes sorted by total journey time

### Map Visualization
- **Interactive Map**: Zoom, pan, and explore India
- **Route Overlay**: Visual route paths with color-coded markers
  - 🟢 Green: Departure station
  - 🔴 Red: Destination station
  - 🟠 Orange: Transfer points
  - 🔵 Blue: Route line
- **Station Info**: Click markers for station details
- **Auto-fit**: Map automatically centers on selected route

### User Experience
- **Mobile Responsive**: Works on phones, tablets, and desktops
- **Fast Loading**: Dynamic imports for optimal performance
- **Clean Interface**: Modern, intuitive design
- **Real-time Feedback**: Loading states and error messages

## 🔧 Configuration

### Environment Variables

Create `frontend/.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:5001
```

### API Port

Change Flask API port in `api.py`:
```python
port = int(os.environ.get('PORT', 5001))
```

Or set environment variable:
```bash
PORT=8000 python3 api.py
```

## 📊 Data Format

### GeoJSON Coordinate Order
All GeoJSON uses `[longitude, latitude]` format as per spec.

### Train Timetable Structure
```json
{
  "12127": {
    "trainNo": 12127,
    "trainName": "Mumbai Pune Intercity",
    "fromStation": "Mumbai CSMT",
    "toStation": "Pune Junction",
    "timetable": [
      {
        "station_code": "CSMT",
        "station_name": "Mumbai CSMT",
        "arrival_time": "Source",
        "departure_time": "07:10",
        "distance_km": "0"
      }
    ]
  }
}
```

## 🛠️ Development

### Backend Development

Run Flask in debug mode:
```bash
FLASK_DEBUG=true python3 api.py
```

### Frontend Development

The Next.js dev server supports:
- Hot reload
- Fast refresh
- TypeScript checking

```bash
cd frontend
npm run dev
```

### Build for Production

Backend:
```bash
# Use a production WSGI server
pip install gunicorn
gunicorn api:app -b 0.0.0.0:5001
```

Frontend:
```bash
cd frontend
npm run build
npm start
```

## 🧪 Testing

### Test Backend API

```bash
# Health check
curl http://localhost:5001/api/health

# Get trains
curl http://localhost:5001/api/trains

# Find routes
curl -X POST http://localhost:5001/api/routes/find \
  -H "Content-Type: application/json" \
  -d '{"from_station": "Mumbai CSMT", "to_station": "Pune Junction"}'
```

### Run Route Finder Tests

```bash
python3 test_route_finder.py
```

## 📱 Mobile Support

The application is fully responsive and works on:
- 📱 Mobile phones (iOS/Android)
- 📱 Tablets
- 💻 Desktop browsers

## 🌐 Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## 🚦 Performance

### Optimizations Implemented
- Dynamic imports for Leaflet (no SSR)
- Client-side rendering for map
- Efficient route algorithm (BFS)
- Single route loading (not all at once)
- Minimal dependencies

## 📝 License

MIT License

## 🙏 Acknowledgments

- Train data sourced from [ProKerala](https://www.prokerala.com/travel/indian-railway/trains/)
- Maps by [OpenStreetMap](https://www.openstreetmap.org/)
- Map library: [Leaflet](https://leafletjs.com/)
- Frontend framework: [Next.js](https://nextjs.org/)

## 📞 Support

For issues or questions:
1. Check existing issues on GitHub
2. Create a new issue with details
3. Include screenshots if applicable

## 🔜 Future Enhancements

- [ ] Train running days (Mon-Sun schedule)
- [ ] Real-time train status integration
- [ ] Seat availability checking
- [ ] Fare calculation
- [ ] Save favorite routes
- [ ] Export routes to PDF
- [ ] Push notifications for trains
- [ ] Offline support with PWA
