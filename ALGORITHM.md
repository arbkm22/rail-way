# Route Finding Algorithm Documentation

## Overview

The route finder uses a modified Breadth-First Search (BFS) algorithm to find optimal train routes between stations, including both direct and multi-hop connections.

## Algorithm Components

### 1. Data Structures

#### Station Index
- **Purpose**: Quick lookup of all trains stopping at a station
- **Structure**: `station_trains[station_name] = [train_info1, train_info2, ...]`
- **Built at initialization**: Iterates through all timetables once

#### Train Timetable
Each train has:
- Train number and name
- List of stops with:
  - Station name and code
  - Arrival time
  - Departure time
  - Distance

### 2. Direct Route Search

**Algorithm**: Linear scan through all trains
```
For each train:
    Find if both source and destination are in timetable
    If yes and source comes before destination:
        Add to direct routes
```

**Time Complexity**: O(T × S) where T = number of trains, S = average stops per train

### 3. Multi-Hop Route Search

**Algorithm**: Modified BFS with timing constraints

```
Initialize queue with all trains from source station

While queue not empty:
    current_station, arrival_time, path, total_duration = dequeue()
    
    If reached destination:
        Add to results
        Continue (to find other routes)
    
    If max_hops reached:
        Continue
    
    For each train at current_station:
        departure_time = train's departure from current_station
        
        # Timing constraint check
        waiting_time = departure_time - arrival_time
        if waiting_time > max_waiting_hours:
            Skip this train
        
        For each destination reachable from this train:
            if not already visited in this path:
                new_path = path + [segment]
                enqueue(destination, arrival_time, new_path, new_duration)
```

**Key Features**:
- **Cycle Prevention**: Tracks visited stations per path
- **Timing Validation**: Ensures realistic waiting times
- **Early Termination**: Can limit search depth with max_hops

**Time Complexity**: O(S^H × T) where:
- S = number of stations
- H = maximum hops allowed
- T = average trains per station

### 4. Time Handling

#### Time Parsing
```python
"14:30" → 870 minutes from midnight
"23:45" → 1425 minutes from midnight
```

#### Day Crossover Handling
```python
If departure = 23:00 (1380 min) and arrival = 02:00 (120 min):
    diff = 120 - 1380 = -1260
    Since negative, add 24 hours: -1260 + 1440 = 180 minutes (3 hours)
```

This handles overnight journeys correctly.

#### Waiting Time Calculation
```python
waiting_time = departure_time - arrival_time
if waiting_time < 0:
    waiting_time += 24 * 60  # Next day departure
```

### 5. Result Ranking

Routes are sorted by:
1. Total journey duration (primary)
2. Number of changes (implicit - affects duration via waiting time)

```python
routes.sort(key=lambda x: x['total_duration'])
```

## Example Walkthrough

### Scenario: Pune → Ranchi

#### Step 1: Direct Search
```
Search all trains for (Pune Junction → Ranchi Junction):
  Train 12875: Pune Hatia SF Express
    - Pune (20:30) → Ranchi (05:30)
    - Duration: 9h 0m
    ✓ Add to results
```

#### Step 2: Multi-hop Search
```
Start BFS from Pune Junction:

Iteration 1:
  Trains from Pune:
    - Train 12123: Pune → Nagpur (14:30 → 04:30, 14h)
      Queue: [(Nagpur, 04:30, [Pune→Nagpur], 14h)]
    - Train 12875: Pune → Multiple stops
      Queue: [..., (Raipur, 15:00, [Pune→Raipur], 18.5h), ...]

Iteration 2:
  Dequeue: (Nagpur, 04:30, [Pune→Nagpur], 14h)
  Trains from Nagpur:
    - Train 18029: Nagpur → Bilaspur (06:00 → 15:00)
      Waiting: 06:00 - 04:30 = 1.5h ✓ (< 4h)
      Queue: [..., (Bilaspur, 15:00, [Pune→Nagpur, Nagpur→Bilaspur], 24.5h)]

Continue until all paths explored or max_hops reached...
```

### Constraints Applied

1. **Max Waiting Time (4 hours)**
   ```
   If train arrives at 10:00 and next train departs at 15:00:
     Waiting = 5 hours → REJECTED
   ```

2. **No Cycles**
   ```
   Path: [Pune → Nagpur → Bilaspur]
   Next: Nagpur → REJECTED (already visited)
   ```

3. **Max Hops (3)**
   ```
   Path: [A → B → C → D]
   Length = 3 hops → Don't explore further from D
   ```

## Optimizations

### 1. Early Termination
- Stop exploring paths longer than best direct route found
- Skip paths that exceed reasonable duration

### 2. State Deduplication
```python
state = (current_station, len(path))
if state in visited:
    skip
```

Avoids exploring same state multiple times.

### 3. Efficient Station Lookup
- Pre-built index eliminates need to scan all trains
- O(1) lookup for trains at a station

## Complexity Analysis

### Space Complexity
- Station Index: O(T × S)
- BFS Queue: O(S^H) in worst case

### Time Complexity
- Direct Search: O(T × S)
- Multi-hop Search: O(S^H × T × S)
- Total: O(S^(H+1) × T)

### Practical Performance
With:
- T = 8 trains (sample data)
- S = 32 stations
- H = 3 max hops
- Average 10 stops per train

Typical search completes in < 1 second.

## Future Improvements

1. **A* Search**
   - Use heuristic (geographic distance) to prioritize paths
   - Faster convergence to optimal route

2. **Dynamic Programming**
   - Memoize intermediate results
   - Avoid recomputing same subproblems

3. **Bidirectional Search**
   - Search from both source and destination
   - Meet in the middle for faster results

4. **Parallel Processing**
   - Explore multiple paths simultaneously
   - Useful for large datasets

5. **Time Windows**
   - Specify departure time preference
   - Find routes starting within time window

6. **Train Frequency**
   - Account for trains running on specific days
   - Weekly schedule patterns

## Testing Strategy

Tests validate:
- ✓ Direct route discovery
- ✓ Multi-hop path finding
- ✓ Timing constraint enforcement
- ✓ Cycle prevention
- ✓ Result sorting
- ✓ Edge case handling

See `test_route_finder.py` for complete test suite.
