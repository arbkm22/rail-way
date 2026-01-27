/**
 * API client for the Railway Route Finder
 * Uses Next.js API routes instead of external Flask backend
 */

export interface RouteSegment {
  train_no: string;
  train_name: string;
  from_station: string;
  to_station: string;
  departure: string;
  arrival: string;
  duration: string;
  duration_minutes: number;
  waiting_time?: string;
  waiting_time_minutes?: number;
  from_coordinates?: {
    lat: number;
    lon: number;
  };
  to_coordinates?: {
    lat: number;
    lon: number;
  };
}

export interface Route {
  route_type: string;
  total_duration: string;
  total_duration_minutes: number;
  num_changes: number;
  segments: RouteSegment[];
  geometry: {
    type: string;
    geometry: {
      type: string;
      coordinates: number[][];
    };
    properties: {
      route_type: string;
      stations: string[];
    };
  };
}

export interface Station {
  station_name: string;
  has_coordinates: boolean;
}

export interface StationFeature {
  type: string;
  geometry: {
    type: string;
    coordinates: [number, number];
  };
  properties: {
    station_name: string;
    has_coordinates: boolean;
  };
}

export interface StationsResponse {
  type: string;
  features: StationFeature[];
}

export interface RoutesResponse {
  from_station: string;
  to_station: string;
  routes: Route[];
  count?: number;
  message?: string;
}

/**
 * Fetch all stations
 */
export async function fetchStations(): Promise<Station[]> {
  const response = await fetch('/api/stations');
  
  if (!response.ok) {
    throw new Error('Failed to fetch stations');
  }
  
  const data: StationsResponse = await response.json();
  return data.features.map(feature => ({
    station_name: feature.properties.station_name,
    has_coordinates: feature.properties.has_coordinates,
  }));
}

/**
 * Find routes between two stations
 */
export async function findRoutes(
  fromStation: string,
  toStation: string,
  maxWaitingHours: number = 4,
  maxHops: number = 3
): Promise<RoutesResponse> {
  const response = await fetch('/api/routes/find', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from_station: fromStation,
      to_station: toStation,
      max_waiting_hours: maxWaitingHours,
      max_hops: maxHops,
    }),
  });
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ error: 'Unknown error' }));
    throw new Error(errorData.error || 'Failed to find routes');
  }
  
  return response.json();
}
