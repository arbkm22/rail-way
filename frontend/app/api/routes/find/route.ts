import { NextRequest, NextResponse } from 'next/server';
import { TrainRouteFinder, Timetables } from '@/lib/routeFinder';
import timetablesData from '@/public/train_timetables.json';

// Station coordinates mapping
const STATION_COORDINATES: { [key: string]: [number, number] } = {
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
};

function createGeoJSONLineString(coordinates: number[][], properties: any) {
  return {
    type: 'Feature',
    geometry: {
      type: 'LineString',
      coordinates,
    },
    properties,
  };
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { from_station, to_station, max_waiting_hours = 4, max_hops = 3 } = body;
    
    if (!from_station || !to_station) {
      return NextResponse.json(
        { error: 'Please provide both from_station and to_station' },
        { status: 400 }
      );
    }
    
    if (from_station === to_station) {
      return NextResponse.json(
        { error: 'Source and destination cannot be the same' },
        { status: 400 }
      );
    }
    
    const timetables = timetablesData as Timetables;
    const finder = new TrainRouteFinder(timetables);
    
    // Find all routes
    const routes = finder.findAllRoutes(
      from_station,
      to_station,
      max_waiting_hours,
      max_hops
    );
    
    if (routes.length === 0) {
      return NextResponse.json({
        from_station,
        to_station,
        routes: [],
        message: 'No routes found between these stations.',
      });
    }
    
    // Format routes for JSON response with GeoJSON route geometry
    const formattedRoutes = routes.map(route => {
      // Build route coordinates
      const routeCoordinates: number[][] = [];
      const allStationsInRoute: string[] = [];
      
      for (const segment of route.route) {
        const fromCoords = STATION_COORDINATES[segment.from_station];
        const toCoords = STATION_COORDINATES[segment.to_station];
        
        if (fromCoords && routeCoordinates.length === 0) {
          // Add first station
          routeCoordinates.push([fromCoords[1], fromCoords[0]]);
          allStationsInRoute.push(segment.from_station);
        }
        
        if (toCoords) {
          routeCoordinates.push([toCoords[1], toCoords[0]]);
          allStationsInRoute.push(segment.to_station);
        }
      }
      
      const formattedRoute = {
        route_type: route.route_type,
        total_duration: finder.formatDuration(route.total_duration),
        total_duration_minutes: route.total_duration,
        num_changes: route.total_changes,
        segments: route.route.map(segment => {
          const fromCoords = STATION_COORDINATES[segment.from_station];
          const toCoords = STATION_COORDINATES[segment.to_station];
          
          const formattedSegment: any = {
            train_no: segment.train_no,
            train_name: segment.train_name,
            from_station: segment.from_station,
            to_station: segment.to_station,
            departure: segment.departure,
            arrival: segment.arrival,
            duration: finder.formatDuration(segment.duration_minutes),
            duration_minutes: segment.duration_minutes,
          };
          
          if (segment.waiting_time !== undefined) {
            formattedSegment.waiting_time = finder.formatDuration(segment.waiting_time);
            formattedSegment.waiting_time_minutes = segment.waiting_time;
          }
          
          // Add station coordinates
          if (fromCoords) {
            formattedSegment.from_coordinates = {
              lat: fromCoords[0],
              lon: fromCoords[1],
            };
          }
          if (toCoords) {
            formattedSegment.to_coordinates = {
              lat: toCoords[0],
              lon: toCoords[1],
            };
          }
          
          return formattedSegment;
        }),
        geometry: createGeoJSONLineString(routeCoordinates, {
          route_type: route.route_type,
          stations: allStationsInRoute,
        }),
      };
      
      return formattedRoute;
    });
    
    return NextResponse.json({
      from_station,
      to_station,
      routes: formattedRoutes,
      count: formattedRoutes.length,
    });
  } catch (error) {
    console.error('Error finding routes:', error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Failed to find routes' },
      { status: 500 }
    );
  }
}
