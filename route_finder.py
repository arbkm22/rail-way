"""
Route Finder Application
This module implements a train route-finding algorithm that can find both direct
and multi-hop routes between stations with timing constraints.
"""
import json
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from collections import defaultdict, deque
import heapq

class TrainRouteFinder:
    def __init__(self, timetable_file='train_timetables.json'):
        """Initialize the route finder with timetable data."""
        with open(timetable_file, 'r') as f:
            self.timetables = json.load(f)
        
        # Build station-to-train mapping
        self.station_trains = defaultdict(list)
        self._build_station_index()
    
    def _build_station_index(self):
        """Build an index of which trains stop at which stations."""
        for train_no, train_data in self.timetables.items():
            for i, stop in enumerate(train_data['timetable']):
                station = stop['station_name']
                self.station_trains[station].append({
                    'train_no': train_no,
                    'train_name': train_data['trainName'],
                    'stop_index': i,
                    'arrival': stop['arrival_time'],
                    'departure': stop['departure_time'],
                    'timetable': train_data['timetable']
                })
    
    def _parse_time(self, time_str):
        """Parse time string to minutes from midnight."""
        if time_str in ['Source', 'Destination', '']:
            return None
        
        try:
            # Handle HH:MM format
            parts = time_str.split(':')
            hours = int(parts[0])
            minutes = int(parts[1])
            return hours * 60 + minutes
        except (ValueError, IndexError, AttributeError):
            return None
    
    def _time_difference(self, time1_minutes, time2_minutes):
        """Calculate time difference in minutes, handling day crossovers."""
        if time1_minutes is None or time2_minutes is None:
            return None
        
        diff = time2_minutes - time1_minutes
        # If negative, assume next day
        if diff < 0:
            diff += 24 * 60  # Add 24 hours
        return diff
    
    def _format_duration(self, minutes):
        """Format duration in minutes to hours and minutes."""
        hours = minutes // 60
        mins = minutes % 60
        if hours > 0:
            return f"{hours}h {mins}m"
        return f"{mins}m"
    
    def find_direct_trains(self, from_station, to_station):
        """Find all direct trains between two stations."""
        direct_trains = []
        
        for train_no, train_data in self.timetables.items():
            timetable = train_data['timetable']
            
            from_idx = None
            to_idx = None
            
            # Find station indices
            for i, stop in enumerate(timetable):
                if stop['station_name'] == from_station:
                    from_idx = i
                elif stop['station_name'] == to_station and from_idx is not None:
                    to_idx = i
                    break
            
            # If both stations found and from comes before to
            if from_idx is not None and to_idx is not None and from_idx < to_idx:
                from_stop = timetable[from_idx]
                to_stop = timetable[to_idx]
                
                departure = from_stop['departure_time']
                arrival = to_stop['arrival_time']
                
                # Calculate journey time
                dep_minutes = self._parse_time(departure)
                arr_minutes = self._parse_time(arrival)
                duration = self._time_difference(dep_minutes, arr_minutes)
                
                direct_trains.append({
                    'train_no': train_no,
                    'train_name': train_data['trainName'],
                    'from_station': from_station,
                    'to_station': to_station,
                    'departure': departure,
                    'arrival': arrival,
                    'duration_minutes': duration,
                    'stops': to_idx - from_idx + 1,
                    'route_type': 'direct'
                })
        
        return direct_trains
    
    def find_connecting_routes(self, from_station, to_station, max_waiting_hours=4, max_hops=3):
        """
        Find routes with connections between stations.
        
        Args:
            from_station: Starting station
            to_station: Destination station
            max_waiting_hours: Maximum waiting time at intermediate stations
            max_hops: Maximum number of train changes allowed
        
        Returns:
            List of possible routes with connections
        """
        routes = []
        max_waiting_minutes = max_waiting_hours * 60
        
        # BFS to find multi-hop routes
        # State: (current_station, arrival_time_minutes, path, total_duration)
        queue = deque()
        
        # Start from all trains leaving the source station
        if from_station in self.station_trains:
            for train_info in self.station_trains[from_station]:
                departure = self._parse_time(train_info['departure'])
                if departure is None:
                    continue
                
                # Add initial train to queue
                timetable = train_info['timetable']
                stop_idx = train_info['stop_index']
                
                # Check all destinations reachable from this train
                for i in range(stop_idx + 1, len(timetable)):
                    next_stop = timetable[i]
                    next_station = next_stop['station_name']
                    arrival = self._parse_time(next_stop['arrival_time'])
                    
                    if arrival is None:
                        continue
                    
                    journey_time = self._time_difference(departure, arrival)
                    
                    path_segment = {
                        'train_no': train_info['train_no'],
                        'train_name': train_info['train_name'],
                        'from_station': from_station,
                        'to_station': next_station,
                        'departure': train_info['departure'],
                        'arrival': next_stop['arrival_time'],
                        'duration_minutes': journey_time
                    }
                    
                    # If we reached destination
                    if next_station == to_station:
                        routes.append({
                            'route': [path_segment],
                            'total_duration': journey_time,
                            'total_changes': 0,
                            'route_type': 'direct'
                        })
                    elif len([path_segment]) < max_hops:
                        # Add to queue for further exploration
                        queue.append((next_station, arrival, [path_segment], journey_time))
        
        # Explore connections
        visited = set()
        
        while queue:
            current_station, current_arrival, path, total_duration = queue.popleft()
            
            # Skip if we've exceeded max hops
            if len(path) >= max_hops:
                continue
            
            # Create state signature to avoid cycles
            state = (current_station, len(path))
            if state in visited:
                continue
            visited.add(state)
            
            # Look for connecting trains
            if current_station in self.station_trains:
                for train_info in self.station_trains[current_station]:
                    departure = self._parse_time(train_info['departure'])
                    if departure is None:
                        continue
                    
                    # Check waiting time
                    waiting_time = self._time_difference(current_arrival, departure)
                    if waiting_time is None or waiting_time < 0 or waiting_time > max_waiting_minutes:
                        continue
                    
                    # This train is a valid connection
                    timetable = train_info['timetable']
                    stop_idx = train_info['stop_index']
                    
                    # Check all destinations reachable from this train
                    for i in range(stop_idx + 1, len(timetable)):
                        next_stop = timetable[i]
                        next_station = next_stop['station_name']
                        
                        # Avoid going back to already visited stations in this path
                        if any(seg['to_station'] == next_station for seg in path):
                            continue
                        
                        arrival = self._parse_time(next_stop['arrival_time'])
                        if arrival is None:
                            continue
                        
                        journey_time = self._time_difference(departure, arrival)
                        new_total = total_duration + waiting_time + journey_time
                        
                        path_segment = {
                            'train_no': train_info['train_no'],
                            'train_name': train_info['train_name'],
                            'from_station': current_station,
                            'to_station': next_station,
                            'departure': train_info['departure'],
                            'arrival': next_stop['arrival_time'],
                            'duration_minutes': journey_time,
                            'waiting_time': waiting_time
                        }
                        
                        new_path = path + [path_segment]
                        
                        # If we reached destination
                        if next_station == to_station:
                            routes.append({
                                'route': new_path,
                                'total_duration': new_total,
                                'total_changes': len(new_path) - 1,
                                'route_type': f'{len(new_path)}-hop'
                            })
                        elif len(new_path) < max_hops:
                            # Continue exploring
                            queue.append((next_station, arrival, new_path, new_total))
        
        return routes
    
    def find_all_routes(self, from_station, to_station, max_waiting_hours=4, max_hops=3):
        """Find all possible routes (direct and with connections)."""
        # Find direct trains
        direct = self.find_direct_trains(from_station, to_station)
        
        # Find connecting routes
        connecting = self.find_connecting_routes(from_station, to_station, max_waiting_hours, max_hops)
        
        # Combine and sort by total duration
        all_routes = []
        
        # Convert direct trains to route format
        for train in direct:
            all_routes.append({
                'route': [{
                    'train_no': train['train_no'],
                    'train_name': train['train_name'],
                    'from_station': train['from_station'],
                    'to_station': train['to_station'],
                    'departure': train['departure'],
                    'arrival': train['arrival'],
                    'duration_minutes': train['duration_minutes']
                }],
                'total_duration': train['duration_minutes'],
                'total_changes': 0,
                'route_type': 'direct'
            })
        
        # Add connecting routes
        all_routes.extend(connecting)
        
        # Sort by total duration
        all_routes.sort(key=lambda x: x['total_duration'] if x['total_duration'] else float('inf'))
        
        return all_routes
    
    def print_route(self, route):
        """Pretty print a route."""
        print(f"\n{'='*80}")
        print(f"Route Type: {route['route_type'].upper()}")
        print(f"Total Journey Time: {self._format_duration(route['total_duration'])}")
        print(f"Number of Changes: {route['total_changes']}")
        print(f"{'='*80}")
        
        for i, segment in enumerate(route['route'], 1):
            print(f"\nSegment {i}:")
            print(f"  Train: {segment['train_name']} ({segment['train_no']})")
            print(f"  From: {segment['from_station']}")
            print(f"  Departure: {segment['departure']}")
            print(f"  To: {segment['to_station']}")
            print(f"  Arrival: {segment['arrival']}")
            print(f"  Duration: {self._format_duration(segment['duration_minutes'])}")
            
            if 'waiting_time' in segment and i > 1:
                print(f"  Waiting time at {segment['from_station']}: {self._format_duration(segment['waiting_time'])}")
        
        print(f"\n{'='*80}")
    
    def get_all_stations(self):
        """Get list of all unique stations."""
        stations = set()
        for train_data in self.timetables.values():
            for stop in train_data['timetable']:
                stations.add(stop['station_name'])
        return sorted(list(stations))


def main():
    """Main CLI application."""
    print("=" * 80)
    print("INDIAN RAILWAYS ROUTE FINDER")
    print("=" * 80)
    
    # Initialize route finder
    try:
        finder = TrainRouteFinder()
    except FileNotFoundError:
        print("Error: train_timetables.json not found!")
        print("Please run generate_sample_timetables.py first.")
        return
    
    # Get available stations
    stations = finder.get_all_stations()
    print(f"\nAvailable stations ({len(stations)}):")
    for i, station in enumerate(stations, 1):
        print(f"{i}. {station}")
    
    print("\n" + "=" * 80)
    
    # Get user input
    from_station = input("\nEnter starting station (or number): ").strip()
    
    # Check if user entered a number
    try:
        idx = int(from_station) - 1
        if 0 <= idx < len(stations):
            from_station = stations[idx]
    except ValueError:
        pass
    
    to_station = input("Enter destination station (or number): ").strip()
    
    # Check if user entered a number
    try:
        idx = int(to_station) - 1
        if 0 <= idx < len(stations):
            to_station = stations[idx]
    except ValueError:
        pass
    
    # Validate stations
    if from_station not in stations:
        print(f"Error: '{from_station}' is not a valid station.")
        return
    
    if to_station not in stations:
        print(f"Error: '{to_station}' is not a valid station.")
        return
    
    if from_station == to_station:
        print("Error: Source and destination cannot be the same.")
        return
    
    print(f"\nSearching for routes from '{from_station}' to '{to_station}'...")
    max_waiting_hours = 4
    max_hops = 3
    max_changes = max(0, max_hops - 1)
    print(f"Maximum waiting time at intermediate stations: {max_waiting_hours} hours")
    print(f"Maximum number of train changes: {max_changes}")
    
    # Find routes
    routes = finder.find_all_routes(
        from_station,
        to_station,
        max_waiting_hours=max_waiting_hours,
        max_hops=max_hops,
    )
    
    if not routes:
        print(f"\nNo routes found from '{from_station}' to '{to_station}'.")
        return
    
    print(f"\nFound {len(routes)} route(s):\n")
    
    # Print all routes
    for i, route in enumerate(routes, 1):
        print(f"\n{'#'*80}")
        print(f"OPTION {i}")
        finder.print_route(route)
    
    print("\n" + "=" * 80)
    print("Search completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()
