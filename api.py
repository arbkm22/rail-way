"""
Flask REST API for Indian Railways Route Finder
Provides JSON endpoints for train routes, stations, and route finding
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from route_finder import TrainRouteFinder
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for Next.js frontend

# Initialize the route finder
route_finder = None

def init_route_finder():
    """Initialize the route finder with timetable data."""
    global route_finder
    if route_finder is None:
        try:
            route_finder = TrainRouteFinder()
        except FileNotFoundError:
            route_finder = None
    return route_finder

def create_geojson_point(lat, lon, properties=None):
    """Create a GeoJSON Point feature."""
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [lon, lat]  # GeoJSON uses [longitude, latitude]
        },
        "properties": properties or {}
    }

def create_geojson_linestring(coordinates, properties=None):
    """Create a GeoJSON LineString feature."""
    return {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": coordinates  # Array of [lon, lat] pairs
        },
        "properties": properties or {}
    }

# Station coordinates mapping
STATION_COORDINATES = {
    "Ahmadnagar": [19.0948, 74.7480],
    "Akola Junction": [20.7002, 77.0082],
    "Badnera Junction": [20.9320, 77.0590],
    "Bhusaval Junction": [21.0444, 75.7847],
    "Bilaspur Junction": [22.0797, 82.1409],
    "Chakradharpur": [22.7000, 85.6300],
    "Danapur Junction": [25.6093, 85.0461],
    "Daund Junction": [18.4651, 74.5844],
    "Dhanbad Junction": [23.7644, 86.4305],
    "Durg Junction": [21.1904, 81.2849],
    "Gaya Junction": [24.7955, 84.9994],
    "Gondia Junction": [21.4570, 80.1958],
    "Hatia": [23.3441, 85.3096],
    "Howrah Junction": [22.5826, 88.3426],
    "Jalgaon Junction": [21.0077, 75.5626],
    "Jharsuguda Junction": [21.8549, 84.0070],
    "Kalyan Junction": [19.2403, 73.1305],
    "Kharagpur Junction": [22.3460, 87.3212],
    "Kopargaon": [19.8826, 74.4761],
    "Lonavala": [18.7537, 73.4086],
    "Manmad Junction": [20.2536, 74.4386],
    "Mumbai CSMT": [18.9398, 72.8355],
    "Mumbai LTT": [19.0658, 72.8919],
    "Muri Junction": [23.2340, 85.4960],
    "Nagpur Junction": [21.1458, 79.0882],
    "Nashik Road": [20.1110, 73.7906],
    "Pune Junction": [18.5284, 73.8742],
    "Raigarh": [21.8974, 83.3950],
    "Raipur Junction": [21.2514, 81.6296],
    "Ranchi Junction": [23.3629, 85.3222],
    "Rourkela Junction": [22.2604, 84.8536],
    "Tatanagar Junction": [22.8046, 86.2029]
}

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    finder = init_route_finder()
    return jsonify({
        'status': 'healthy',
        'data_loaded': finder is not None
    })

@app.route('/api/trains', methods=['GET'])
def get_trains():
    """Get list of all trains."""
    finder = init_route_finder()
    if finder is None:
        return jsonify({'error': 'Timetable data not found'}), 500
    
    trains = []
    for train_no, train_data in finder.timetables.items():
        trains.append({
            'train_no': train_no,
            'train_name': train_data['trainName'],
            'from_station': train_data['fromStation'],
            'to_station': train_data['toStation'],
            'num_stops': len(train_data['timetable'])
        })
    
    return jsonify({
        'trains': trains,
        'count': len(trains)
    })

@app.route('/api/trains/<train_id>/route', methods=['GET'])
def get_train_route(train_id):
    """Get train route as GeoJSON LineString."""
    finder = init_route_finder()
    if finder is None:
        return jsonify({'error': 'Timetable data not found'}), 500
    
    if train_id not in finder.timetables:
        return jsonify({'error': 'Train not found'}), 404
    
    train_data = finder.timetables[train_id]
    timetable = train_data['timetable']
    
    # Build coordinates array for LineString
    coordinates = []
    stations = []
    
    for stop in timetable:
        station_name = stop['station_name']
        if station_name in STATION_COORDINATES:
            lat, lon = STATION_COORDINATES[station_name]
            coordinates.append([lon, lat])  # GeoJSON format: [longitude, latitude]
            stations.append({
                'station_name': station_name,
                'station_code': stop['station_code'],
                'arrival_time': stop['arrival_time'],
                'departure_time': stop['departure_time'],
                'distance_km': stop['distance_km']
            })
    
    # Create GeoJSON LineString
    geojson = create_geojson_linestring(coordinates, {
        'train_no': train_id,
        'train_name': train_data['trainName'],
        'from_station': train_data['fromStation'],
        'to_station': train_data['toStation'],
        'stations': stations
    })
    
    return jsonify(geojson)

@app.route('/api/stations', methods=['GET'])
def get_stations():
    """Get all stations as GeoJSON FeatureCollection."""
    finder = init_route_finder()
    if finder is None:
        return jsonify({'error': 'Timetable data not found'}), 500
    
    # Get all unique stations from route finder
    all_stations = finder.get_all_stations()
    
    # Filter by train_id if provided
    train_id = request.args.get('train_id')
    if train_id:
        if train_id not in finder.timetables:
            return jsonify({'error': 'Train not found'}), 404
        
        train_data = finder.timetables[train_id]
        all_stations = [stop['station_name'] for stop in train_data['timetable']]
    
    # Create GeoJSON features for each station
    features = []
    for station_name in all_stations:
        if station_name in STATION_COORDINATES:
            lat, lon = STATION_COORDINATES[station_name]
            feature = create_geojson_point(lat, lon, {
                'station_name': station_name,
                'has_coordinates': True
            })
            features.append(feature)
    
    # Return as FeatureCollection
    return jsonify({
        'type': 'FeatureCollection',
        'features': features
    })

@app.route('/api/routes/find', methods=['POST'])
def find_routes():
    """Find routes between two stations."""
    finder = init_route_finder()
    if finder is None:
        return jsonify({'error': 'Timetable data not found'}), 500
    
    data = request.get_json()
    from_station = data.get('from_station')
    to_station = data.get('to_station')
    max_waiting_hours = int(data.get('max_waiting_hours', 4))
    max_hops = int(data.get('max_hops', 3))
    
    if not from_station or not to_station:
        return jsonify({'error': 'Please provide both from_station and to_station'}), 400
    
    if from_station == to_station:
        return jsonify({'error': 'Source and destination cannot be the same'}), 400
    
    try:
        # Find all routes
        routes = finder.find_all_routes(
            from_station, 
            to_station,
            max_waiting_hours=max_waiting_hours,
            max_hops=max_hops
        )
        
        if not routes:
            return jsonify({
                'from_station': from_station,
                'to_station': to_station,
                'routes': [],
                'message': 'No routes found between these stations.'
            })
        
        # Format routes for JSON response with GeoJSON route geometry
        formatted_routes = []
        for route in routes:
            # Build route coordinates
            route_coordinates = []
            all_stations_in_route = []
            
            for segment in route['route']:
                from_coords = STATION_COORDINATES.get(segment['from_station'])
                to_coords = STATION_COORDINATES.get(segment['to_station'])
                
                if from_coords and not route_coordinates:
                    # Add first station
                    route_coordinates.append([from_coords[1], from_coords[0]])
                    all_stations_in_route.append(segment['from_station'])
                
                if to_coords:
                    route_coordinates.append([to_coords[1], to_coords[0]])
                    all_stations_in_route.append(segment['to_station'])
            
            formatted_route = {
                'route_type': route['route_type'],
                'total_duration': finder._format_duration(route['total_duration']),
                'total_duration_minutes': route['total_duration'],
                'num_changes': route['total_changes'],
                'segments': [],
                'geometry': create_geojson_linestring(route_coordinates, {
                    'route_type': route['route_type'],
                    'stations': all_stations_in_route
                })
            }
            
            for segment in route['route']:
                formatted_segment = {
                    'train_no': segment['train_no'],
                    'train_name': segment['train_name'],
                    'from_station': segment['from_station'],
                    'to_station': segment['to_station'],
                    'departure': segment['departure'],
                    'arrival': segment['arrival'],
                    'duration': finder._format_duration(segment['duration_minutes']),
                    'duration_minutes': segment['duration_minutes']
                }
                
                if 'waiting_time' in segment:
                    formatted_segment['waiting_time'] = finder._format_duration(segment['waiting_time'])
                    formatted_segment['waiting_time_minutes'] = segment['waiting_time']
                
                # Add station coordinates
                from_coords = STATION_COORDINATES.get(segment['from_station'])
                to_coords = STATION_COORDINATES.get(segment['to_station'])
                
                if from_coords:
                    formatted_segment['from_coordinates'] = {
                        'lat': from_coords[0],
                        'lon': from_coords[1]
                    }
                if to_coords:
                    formatted_segment['to_coordinates'] = {
                        'lat': to_coords[0],
                        'lon': to_coords[1]
                    }
                
                formatted_route['segments'].append(formatted_segment)
            
            formatted_routes.append(formatted_route)
        
        return jsonify({
            'from_station': from_station,
            'to_station': to_station,
            'routes': formatted_routes,
            'count': len(formatted_routes)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
