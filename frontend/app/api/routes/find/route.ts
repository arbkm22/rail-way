import { NextRequest, NextResponse } from 'next/server';
import { TrainRouteFinder, Timetables } from '@/lib/routeFinder';
import { STATION_COORDINATES } from '@/lib/constants';
import timetablesData from '@/public/train_timetables.json';

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
