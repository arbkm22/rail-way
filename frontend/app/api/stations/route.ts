import { NextResponse } from 'next/server';
import { TrainRouteFinder, Timetables } from '@/lib/routeFinder';
import { STATION_COORDINATES } from '@/lib/constants';
import timetablesData from '@/public/train_timetables.json';

export async function GET() {
  try {
    const timetables = timetablesData as Timetables;
    const finder = new TrainRouteFinder(timetables);
    
    // Get all unique stations
    const allStations = finder.getAllStations();
    
    // Create GeoJSON features for each station
    const features = allStations
      .filter(stationName => stationName in STATION_COORDINATES)
      .map(stationName => {
        const [lat, lon] = STATION_COORDINATES[stationName];
        return {
          type: 'Feature',
          geometry: {
            type: 'Point',
            coordinates: [lon, lat], // GeoJSON uses [longitude, latitude]
          },
          properties: {
            station_name: stationName,
            has_coordinates: true,
          },
        };
      });
    
    // Return as FeatureCollection
    return NextResponse.json({
      type: 'FeatureCollection',
      features,
    });
  } catch (error) {
    console.error('Error fetching stations:', error);
    return NextResponse.json(
      { error: 'Failed to fetch stations' },
      { status: 500 }
    );
  }
}
