# Web Application Guide

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure Sample Data Exists**
   ```bash
   # Check if train_timetables.json exists
   ls train_timetables.json
   
   # If not found, generate sample data:
   python3 generate_sample_timetables.py
   ```

3. **Start the Web Server**
   ```bash
   # For development (with debug mode)
   FLASK_DEBUG=true python3 app.py
   
   # For production (without debug mode - recommended)
   python3 app.py
   ```
   
   **Security Note**: Debug mode should never be enabled in production as it can expose sensitive information and allow arbitrary code execution.

4. **Access the Application**
   
   Open your browser and go to: http://localhost:5000

## Features

### Station Selection
- Choose your starting station from the dropdown menu
- Choose your destination station from the dropdown menu
- All 32+ stations in the sample dataset are available

### Advanced Options
- **Max Waiting Time (hours)**: Set the maximum time you're willing to wait at intermediate stations (default: 4 hours)
- **Max Train Changes**: Set the maximum number of train changes you're willing to make (default: 3)

### Results Display
The application shows:
- **Direct routes**: Trains that go directly from source to destination (marked with green "direct" badge)
- **Multi-hop routes**: Routes requiring one or more train changes (marked with yellow badge showing number of hops)
- **Journey time**: Total travel time including waiting periods
- **Number of changes**: How many times you need to switch trains
- **Detailed segments**: For each leg of the journey:
  - Train name and number
  - Departure and arrival stations
  - Departure and arrival times
  - Duration of each segment
  - Waiting time at intermediate stations

### Results Sorting
Routes are automatically sorted by total journey time, with the fastest option shown first.

## API Endpoint

The web app also provides a JSON API endpoint for programmatic access:

### POST /find_routes

**Request Body:**
```json
{
  "from_station": "Pune Junction",
  "to_station": "Ranchi Junction",
  "max_waiting_hours": 4,
  "max_hops": 3
}
```

**Response:**
```json
{
  "from_station": "Pune Junction",
  "to_station": "Ranchi Junction",
  "routes": [
    {
      "route_type": "direct",
      "total_duration": "9h 0m",
      "num_changes": 0,
      "segments": [
        {
          "train_no": "12875",
          "train_name": "Pune Hatia SF Express",
          "from_station": "Pune Junction",
          "to_station": "Ranchi Junction",
          "departure": "20:30",
          "arrival": "05:30",
          "duration": "9h 0m"
        }
      ]
    }
  ]
}
```

## Troubleshooting

### Port Already in Use
If you get an error that port 5000 is already in use:

1. Find the process using the port:
   ```bash
   lsof -i :5000
   ```

2. Kill the process or change the port in `app.py`:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
   ```

### Timetable Data Not Found
If you see an error about missing timetable data:

```bash
python3 generate_sample_timetables.py
```

### No Routes Found
This can happen if:
- Stations are not connected in the sample data
- Constraints are too strict (try increasing max_waiting_hours or max_hops)
- Stations don't exist in the dataset

## Production Deployment

For production deployment, use a proper WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Or use Docker:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## Technology Stack

- **Backend**: Flask 3.0.0
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Styling**: Custom CSS with gradient design
- **API**: RESTful JSON API
- **Data**: JSON-based timetable storage

## Browser Compatibility

The web app works on all modern browsers:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
