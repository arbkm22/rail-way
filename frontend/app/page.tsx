'use client';

import { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';
import { fetchStations, findRoutes, Route } from '@/lib/api';

// Dynamically import Map component to avoid SSR issues with Leaflet
const Map = dynamic(() => import('@/components/Map'), {
  ssr: false,
  loading: () => (
    <div className="w-full h-full flex items-center justify-center bg-gray-100">
      <p className="text-gray-500">Loading map...</p>
    </div>
  ),
});

export default function Home() {
  const [stations, setStations] = useState<string[]>([]);
  const [fromStation, setFromStation] = useState('');
  const [toStation, setToStation] = useState('');
  const [maxWaitingHours, setMaxWaitingHours] = useState(4);
  const [maxHops, setMaxHops] = useState(3);
  const [routes, setRoutes] = useState<Route[]>([]);
  const [selectedRoute, setSelectedRoute] = useState<Route | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showAdvanced, setShowAdvanced] = useState(false);

  // Fetch stations on mount
  useEffect(() => {
    fetchStations()
      .then(stationData => {
        const stationNames = stationData.map(s => s.station_name).sort();
        setStations(stationNames);
      })
      .catch(err => {
        console.error('Failed to fetch stations:', err);
        setError('Failed to load stations');
      });
  }, []);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!fromStation || !toStation) {
      setError('Please select both stations');
      return;
    }

    if (fromStation === toStation) {
      setError('Source and destination cannot be the same');
      return;
    }

    setLoading(true);
    setError(null);
    setRoutes([]);
    setSelectedRoute(null);

    try {
      const result = await findRoutes(fromStation, toStation, maxWaitingHours, maxHops);
      
      if (result.routes.length === 0) {
        setError(result.message || 'No routes found between these stations');
      } else {
        setRoutes(result.routes);
        setSelectedRoute(result.routes[0]); // Auto-select first route
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to find routes');
    } finally {
      setLoading(false);
    }
  };

  const swapStations = () => {
    const temp = fromStation;
    setFromStation(toStation);
    setToStation(temp);
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="bg-blue-600 text-white p-4 shadow-lg">
        <div className="container mx-auto">
          <h1 className="text-2xl font-bold flex items-center gap-2">
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
            </svg>
            Indian Railways Route Finder
          </h1>
          <p className="text-sm text-blue-100 mt-1">Plan your train journey across India</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex flex-col lg:flex-row">
        {/* Sidebar */}
        <aside className="w-full lg:w-96 bg-white border-r border-gray-200 overflow-y-auto">
          <div className="p-6">
            <h2 className="text-xl font-semibold mb-4">Route Planner</h2>

            {/* Search Form */}
            <form onSubmit={handleSearch} className="space-y-4">
              {/* Station Selection */}
              <div className="space-y-3">
                <div>
                  <label htmlFor="from_station" className="block text-sm font-medium text-gray-700 mb-1">
                    From
                  </label>
                  <select
                    id="from_station"
                    value={fromStation}
                    onChange={(e) => setFromStation(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  >
                    <option value="">Choose departure station</option>
                    {stations.map(station => (
                      <option key={station} value={station}>{station}</option>
                    ))}
                  </select>
                </div>

                {/* Swap Button */}
                <div className="flex justify-center">
                  <button
                    type="button"
                    onClick={swapStations}
                    className="p-2 text-blue-600 hover:bg-blue-50 rounded-full transition"
                    title="Swap stations"
                  >
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
                    </svg>
                  </button>
                </div>

                <div>
                  <label htmlFor="to_station" className="block text-sm font-medium text-gray-700 mb-1">
                    To
                  </label>
                  <select
                    id="to_station"
                    value={toStation}
                    onChange={(e) => setToStation(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  >
                    <option value="">Choose destination station</option>
                    {stations.map(station => (
                      <option key={station} value={station}>{station}</option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Advanced Options */}
              <div className="border-t pt-4">
                <button
                  type="button"
                  onClick={() => setShowAdvanced(!showAdvanced)}
                  className="flex items-center justify-between w-full text-sm font-medium text-gray-700"
                >
                  <span>Advanced Options</span>
                  <svg
                    className={`w-4 h-4 transition-transform ${showAdvanced ? 'rotate-180' : ''}`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>

                {showAdvanced && (
                  <div className="mt-3 space-y-3">
                    <div>
                      <label htmlFor="max_waiting" className="block text-sm text-gray-600 mb-1">
                        Max Waiting (hours)
                      </label>
                      <input
                        id="max_waiting"
                        type="number"
                        value={maxWaitingHours}
                        onChange={(e) => setMaxWaitingHours(parseInt(e.target.value))}
                        min="1"
                        max="12"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    <div>
                      <label htmlFor="max_hops" className="block text-sm text-gray-600 mb-1">
                        Max Changes
                      </label>
                      <input
                        id="max_hops"
                        type="number"
                        value={maxHops}
                        onChange={(e) => setMaxHops(parseInt(e.target.value))}
                        min="1"
                        max="5"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                  </div>
                )}
              </div>

              {/* Search Button */}
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-600 text-white py-3 rounded-md font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
              >
                {loading ? 'Searching...' : 'Find Routes'}
              </button>
            </form>

            {/* Error Message */}
            {error && (
              <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
                <p className="text-sm text-red-600">{error}</p>
              </div>
            )}

            {/* Results */}
            {routes.length > 0 && (
              <div className="mt-6">
                <h3 className="text-lg font-semibold mb-3">
                  Found {routes.length} route{routes.length !== 1 ? 's' : ''}
                </h3>
                <div className="space-y-3">
                  {routes.map((route, index) => (
                    <div
                      key={index}
                      onClick={() => setSelectedRoute(route)}
                      className={`p-4 border rounded-lg cursor-pointer transition ${
                        selectedRoute === route
                          ? 'border-blue-500 bg-blue-50'
                          : 'border-gray-200 hover:border-blue-300'
                      }`}
                    >
                      <div className="flex justify-between items-start mb-2">
                        <span className="text-xs font-semibold text-blue-600 uppercase">
                          {route.route_type}
                        </span>
                        <span className="text-sm font-medium">{route.total_duration}</span>
                      </div>
                      <p className="text-sm text-gray-600">
                        {route.num_changes} change{route.num_changes !== 1 ? 's' : ''}
                      </p>
                      <div className="mt-2 space-y-1">
                        {route.segments.map((segment, segIndex) => (
                          <div key={segIndex} className="text-xs text-gray-500">
                            {segment.train_name} ({segment.train_no})
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </aside>

        {/* Map */}
        <div className="flex-1 h-[500px] lg:h-auto">
          <Map selectedRoute={selectedRoute} />
        </div>
      </main>
    </div>
  );
}

