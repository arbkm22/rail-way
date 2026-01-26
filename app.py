"""
Flask Web Application for Indian Railways Route Finder
"""
from flask import Flask, render_template, request, jsonify
from route_finder import TrainRouteFinder
import os

app = Flask(__name__)

# Initialize the route finder
route_finder = None

def init_route_finder():
    """Initialize the route finder with timetable data."""
    global route_finder
    if route_finder is None:
        try:
            route_finder = TrainRouteFinder()
        except FileNotFoundError:
            # If timetable file doesn't exist, return None
            route_finder = None
    return route_finder

@app.route('/')
def index():
    """Render the main page."""
    finder = init_route_finder()
    if finder is None:
        return render_template('index.html', error="Timetable data not found. Please generate sample data first.")
    
    # Get all unique stations
    stations = sorted(set(finder.station_trains.keys()))
    return render_template('index.html', stations=stations)

@app.route('/find_routes', methods=['POST'])
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
        return jsonify({'error': 'Please select both stations'}), 400
    
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
        
        # Format routes for JSON response
        formatted_routes = []
        for route in routes:
            formatted_route = {
                'route_type': route['route_type'],
                'total_duration': finder._format_duration(route['total_duration']),
                'num_changes': route['total_changes'],
                'segments': []
            }
            
            for segment in route['route']:
                formatted_segment = {
                    'train_no': segment['train_no'],
                    'train_name': segment['train_name'],
                    'from_station': segment['from_station'],
                    'to_station': segment['to_station'],
                    'departure': segment['departure'],
                    'arrival': segment['arrival'],
                    'duration': finder._format_duration(segment['duration_minutes'])
                }
                
                if 'waiting_time' in segment:
                    formatted_segment['waiting_time'] = finder._format_duration(segment['waiting_time'])
                
                formatted_route['segments'].append(formatted_segment)
            
            formatted_routes.append(formatted_route)
        
        return jsonify({
            'from_station': from_station,
            'to_station': to_station,
            'routes': formatted_routes
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
