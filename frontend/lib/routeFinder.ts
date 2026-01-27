/**
 * Route Finder Logic
 * TypeScript port of the Python route_finder.py
 */

export interface Stop {
  station_code: string;
  station_name: string;
  arrival_time: string;
  departure_time: string;
  distance_km: string;
}

export interface TrainData {
  trainNo: number;
  trainName: string;
  fromStation: string;
  toStation: string;
  timetable: Stop[];
}

export interface Timetables {
  [trainNo: string]: TrainData;
}

export interface TrainInfo {
  train_no: string;
  train_name: string;
  stop_index: number;
  arrival: string;
  departure: string;
  timetable: Stop[];
}

export interface RouteSegment {
  train_no: string;
  train_name: string;
  from_station: string;
  to_station: string;
  departure: string;
  arrival: string;
  duration_minutes: number;
  waiting_time?: number;
}

export interface Route {
  route: RouteSegment[];
  total_duration: number;
  total_changes: number;
  route_type: string;
}

export class TrainRouteFinder {
  private timetables: Timetables;
  private stationTrains: Map<string, TrainInfo[]>;

  constructor(timetables: Timetables) {
    this.timetables = timetables;
    this.stationTrains = new Map();
    this.buildStationIndex();
  }

  private buildStationIndex(): void {
    for (const [trainNo, trainData] of Object.entries(this.timetables)) {
      trainData.timetable.forEach((stop, i) => {
        const station = stop.station_name;
        if (!this.stationTrains.has(station)) {
          this.stationTrains.set(station, []);
        }
        this.stationTrains.get(station)!.push({
          train_no: trainNo,
          train_name: trainData.trainName,
          stop_index: i,
          arrival: stop.arrival_time,
          departure: stop.departure_time,
          timetable: trainData.timetable,
        });
      });
    }
  }

  private parseTime(timeStr: string): number | null {
    if (timeStr === 'Source' || timeStr === 'Destination' || !timeStr) {
      return null;
    }

    try {
      const parts = timeStr.split(':');
      const hours = parseInt(parts[0], 10);
      const minutes = parseInt(parts[1], 10);
      return hours * 60 + minutes;
    } catch {
      return null;
    }
  }

  private timeDifference(time1Minutes: number | null, time2Minutes: number | null): number | null {
    if (time1Minutes === null || time2Minutes === null) {
      return null;
    }

    let diff = time2Minutes - time1Minutes;
    // If negative, assume next day
    if (diff < 0) {
      diff += 24 * 60; // Add 24 hours
    }
    return diff;
  }

  formatDuration(minutes: number): string {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (hours > 0) {
      return `${hours}h ${mins}m`;
    }
    return `${mins}m`;
  }

  findDirectTrains(fromStation: string, toStation: string): Route[] {
    const directTrains: Route[] = [];

    for (const [trainNo, trainData] of Object.entries(this.timetables)) {
      const timetable = trainData.timetable;

      let fromIdx: number | null = null;
      let toIdx: number | null = null;

      // Find station indices
      for (let i = 0; i < timetable.length; i++) {
        if (timetable[i].station_name === fromStation) {
          fromIdx = i;
        } else if (timetable[i].station_name === toStation && fromIdx !== null) {
          toIdx = i;
          break;
        }
      }

      // If both stations found and from comes before to
      if (fromIdx !== null && toIdx !== null && fromIdx < toIdx) {
        const fromStop = timetable[fromIdx];
        const toStop = timetable[toIdx];

        const departure = fromStop.departure_time;
        const arrival = toStop.arrival_time;

        // Calculate journey time
        const depMinutes = this.parseTime(departure);
        const arrMinutes = this.parseTime(arrival);
        const duration = this.timeDifference(depMinutes, arrMinutes);

        if (duration !== null) {
          directTrains.push({
            route: [
              {
                train_no: trainNo,
                train_name: trainData.trainName,
                from_station: fromStation,
                to_station: toStation,
                departure,
                arrival,
                duration_minutes: duration,
              },
            ],
            total_duration: duration,
            total_changes: 0,
            route_type: 'direct',
          });
        }
      }
    }

    return directTrains;
  }

  findConnectingRoutes(
    fromStation: string,
    toStation: string,
    maxWaitingHours: number = 4,
    maxHops: number = 3
  ): Route[] {
    const routes: Route[] = [];
    const maxWaitingMinutes = maxWaitingHours * 60;

    // BFS to find multi-hop routes
    interface QueueItem {
      currentStation: string;
      currentArrival: number;
      path: RouteSegment[];
      totalDuration: number;
    }

    const queue: QueueItem[] = [];

    // Start from all trains leaving the source station
    const sourceTrains = this.stationTrains.get(fromStation);
    if (sourceTrains) {
      for (const trainInfo of sourceTrains) {
        const departure = this.parseTime(trainInfo.departure);
        if (departure === null) continue;

        const timetable = trainInfo.timetable;
        const stopIdx = trainInfo.stop_index;

        // Check all destinations reachable from this train
        for (let i = stopIdx + 1; i < timetable.length; i++) {
          const nextStop = timetable[i];
          const nextStation = nextStop.station_name;
          const arrival = this.parseTime(nextStop.arrival_time);

          if (arrival === null) continue;

          const journeyTime = this.timeDifference(departure, arrival);
          if (journeyTime === null) continue;

          const pathSegment: RouteSegment = {
            train_no: trainInfo.train_no,
            train_name: trainInfo.train_name,
            from_station: fromStation,
            to_station: nextStation,
            departure: trainInfo.departure,
            arrival: nextStop.arrival_time,
            duration_minutes: journeyTime,
          };

          // Skip if we reached destination (handled by direct routes)
          if (nextStation === toStation) {
            continue;
          } else if (1 < maxHops) {
            queue.push({
              currentStation: nextStation,
              currentArrival: arrival,
              path: [pathSegment],
              totalDuration: journeyTime,
            });
          }
        }
      }
    }

    // Explore connections
    const visited = new Set<string>();

    while (queue.length > 0) {
      const { currentStation, currentArrival, path, totalDuration } = queue.shift()!;

      // Skip if we've exceeded max hops
      if (path.length >= maxHops) continue;

      // Create state signature to avoid cycles
      const state = `${currentStation}-${path.length}`;
      if (visited.has(state)) continue;
      visited.add(state);

      // Look for connecting trains
      const connectingTrains = this.stationTrains.get(currentStation);
      if (connectingTrains) {
        for (const trainInfo of connectingTrains) {
          const departure = this.parseTime(trainInfo.departure);
          if (departure === null) continue;

          // Avoid staying on the same train
          if (path.length > 0 && trainInfo.train_no === path[path.length - 1].train_no) {
            continue;
          }

          // Check waiting time
          const waitingTime = this.timeDifference(currentArrival, departure);
          if (waitingTime === null || waitingTime < 0 || waitingTime > maxWaitingMinutes) {
            continue;
          }

          const timetable = trainInfo.timetable;
          const stopIdx = trainInfo.stop_index;

          // Track visited stations in this path
          const visitedStations = new Set<string>([currentStation]);
          for (const seg of path) {
            visitedStations.add(seg.from_station);
            visitedStations.add(seg.to_station);
          }

          // Check all destinations reachable from this train
          for (let i = stopIdx + 1; i < timetable.length; i++) {
            const nextStop = timetable[i];
            const nextStation = nextStop.station_name;

            // Avoid going back to already visited stations
            if (visitedStations.has(nextStation)) continue;

            const arrival = this.parseTime(nextStop.arrival_time);
            if (arrival === null) continue;

            const journeyTime = this.timeDifference(departure, arrival);
            if (journeyTime === null) continue;

            const newTotal = totalDuration + waitingTime + journeyTime;

            const pathSegment: RouteSegment = {
              train_no: trainInfo.train_no,
              train_name: trainInfo.train_name,
              from_station: currentStation,
              to_station: nextStation,
              departure: trainInfo.departure,
              arrival: nextStop.arrival_time,
              duration_minutes: journeyTime,
              waiting_time: waitingTime,
            };

            const newPath = [...path, pathSegment];

            // If we reached destination
            if (nextStation === toStation) {
              routes.push({
                route: newPath,
                total_duration: newTotal,
                total_changes: newPath.length - 1,
                route_type: `${newPath.length}-hop`,
              });
            } else if (newPath.length < maxHops) {
              // Continue exploring
              queue.push({
                currentStation: nextStation,
                currentArrival: arrival,
                path: newPath,
                totalDuration: newTotal,
              });
            }
          }
        }
      }
    }

    return routes;
  }

  findAllRoutes(
    fromStation: string,
    toStation: string,
    maxWaitingHours: number = 4,
    maxHops: number = 3
  ): Route[] {
    // Find direct trains
    const direct = this.findDirectTrains(fromStation, toStation);

    // Find connecting routes
    const connecting = this.findConnectingRoutes(fromStation, toStation, maxWaitingHours, maxHops);

    // Combine and sort by total duration
    const allRoutes = [...direct, ...connecting];

    // Sort by total duration
    allRoutes.sort((a, b) => a.total_duration - b.total_duration);

    return allRoutes;
  }

  getAllStations(): string[] {
    const stations = new Set<string>();
    for (const trainData of Object.values(this.timetables)) {
      for (const stop of trainData.timetable) {
        stations.add(stop.station_name);
      }
    }
    return Array.from(stations).sort();
  }
}
