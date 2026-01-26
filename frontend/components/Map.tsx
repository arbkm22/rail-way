'use client';

import { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { Route } from '@/lib/api';

// Fix for default marker icons in Next.js
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

interface MapProps {
  selectedRoute: Route | null;
}

export default function Map({ selectedRoute }: MapProps) {
  const mapRef = useRef<L.Map | null>(null);
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const markersRef = useRef<L.Marker[]>([]);
  const polylinesRef = useRef<L.Polyline[]>([]);

  // Initialize map
  useEffect(() => {
    if (!mapContainerRef.current || mapRef.current) return;

    // Create map centered on India
    const map = L.map(mapContainerRef.current).setView([20.5937, 78.9629], 5);

    // Add OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 19,
      minZoom: 4,
    }).addTo(map);

    mapRef.current = map;

    // Cleanup on unmount
    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, []);

  // Update route visualization when selectedRoute changes
  useEffect(() => {
    if (!mapRef.current) return;

    const map = mapRef.current;

    // Clear existing markers and polylines
    markersRef.current.forEach(marker => map.removeLayer(marker));
    polylinesRef.current.forEach(polyline => map.removeLayer(polyline));
    markersRef.current = [];
    polylinesRef.current = [];

    if (!selectedRoute) {
      // Reset view to India
      map.setView([20.5937, 78.9629], 5);
      return;
    }

    // Create custom icons
    const createIcon = (color: string) => {
      return L.divIcon({
        className: 'custom-marker',
        html: `<div style="background-color: ${color}; width: 12px; height: 12px; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>`,
        iconSize: [16, 16],
        iconAnchor: [8, 8],
      });
    };

    const departureIcon = createIcon('#10b981'); // Green
    const destinationIcon = createIcon('#ef4444'); // Red
    const transferIcon = createIcon('#f59e0b'); // Orange

    // Draw route polyline
    const coordinates: [number, number][] = selectedRoute.geometry.geometry.coordinates.map(
      coord => [coord[1], coord[0]] // Convert [lon, lat] to [lat, lon]
    );

    if (coordinates.length > 0) {
      const polyline = L.polyline(coordinates, {
        color: '#3b82f6',
        weight: 4,
        opacity: 0.7,
      }).addTo(map);
      polylinesRef.current.push(polyline);

      // Fit map to route bounds
      map.fitBounds(polyline.getBounds(), { padding: [50, 50] });
    }

    // Add markers for stations
    const allStations = new Set<string>();
    const transferStations = new Set<string>();

    selectedRoute.segments.forEach((segment, index) => {
      allStations.add(segment.from_station);
      allStations.add(segment.to_station);

      // Mark intermediate stations as transfer points
      if (index > 0) {
        transferStations.add(segment.from_station);
      }
    });

    // Add departure marker
    const firstSegment = selectedRoute.segments[0];
    if (firstSegment.from_coordinates) {
      const marker = L.marker(
        [firstSegment.from_coordinates.lat, firstSegment.from_coordinates.lon],
        { icon: departureIcon }
      )
        .bindPopup(
          `<strong>${firstSegment.from_station}</strong><br/>Departure: ${firstSegment.departure}`
        )
        .addTo(map);
      markersRef.current.push(marker);
    }

    // Add destination marker
    const lastSegment = selectedRoute.segments[selectedRoute.segments.length - 1];
    if (lastSegment.to_coordinates) {
      const marker = L.marker(
        [lastSegment.to_coordinates.lat, lastSegment.to_coordinates.lon],
        { icon: destinationIcon }
      )
        .bindPopup(
          `<strong>${lastSegment.to_station}</strong><br/>Arrival: ${lastSegment.arrival}`
        )
        .addTo(map);
      markersRef.current.push(marker);
    }

    // Add transfer point markers
    selectedRoute.segments.forEach((segment, index) => {
      if (index > 0 && segment.from_coordinates) {
        const marker = L.marker(
          [segment.from_coordinates.lat, segment.from_coordinates.lon],
          { icon: transferIcon }
        )
          .bindPopup(
            `<strong>${segment.from_station}</strong><br/>Transfer Point<br/>Waiting: ${segment.waiting_time || 'N/A'}`
          )
          .addTo(map);
        markersRef.current.push(marker);
      }
    });
  }, [selectedRoute]);

  return (
    <div className="relative w-full h-full">
      <div ref={mapContainerRef} className="w-full h-full" />
      
      {selectedRoute && (
        <div className="absolute bottom-4 left-4 bg-white p-4 rounded-lg shadow-lg z-[1000] max-w-xs">
          <h4 className="font-semibold mb-2">Legend</h4>
          <div className="space-y-2 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-green-500"></div>
              <span>Departure Station</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-red-500"></div>
              <span>Destination</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-orange-500"></div>
              <span>Transfer Point</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-8 h-0.5 bg-blue-500"></div>
              <span>Route</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
