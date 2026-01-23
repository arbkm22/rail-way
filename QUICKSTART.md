# Quick Start Guide

## Get Started in 3 Steps

### Step 1: Verify Sample Data Exists
```bash
# Check if train_timetables.json exists
ls -lh train_timetables.json

# If not, generate it:
python3 generate_sample_timetables.py
```

### Step 2: Run the Application
```bash
# Start the route finder
python3 main.py
```

### Step 3: Find a Route
```
# Example interaction:
Enter starting station (or number): 27
Enter destination station (or number): 30

# This finds routes from Pune to Ranchi
```

## Quick Examples

### Example 1: Direct Route (Pune → Ranchi)
```bash
echo -e "27\n30" | python3 main.py | head -50
```
**Expected**: Direct train via Pune Hatia SF Express (9h journey)

### Example 2: Multi-hop Route (Nagpur → Howrah)
```bash
echo -e "25\n14" | python3 main.py | head -80
```
**Expected**: Multiple options with connections

### Example 3: Run Demo
```bash
./demo.sh
```
**Shows**: Sample query with formatted output

## Test the Implementation

### Run All Tests
```bash
python3 test_route_finder.py
```
**Expected**: All 7 tests pass ✓

### Run Example Queries
```bash
python3 example_usage.py
```
**Shows**: Programmatic API usage examples

## Station Numbers Reference

Quick reference for common stations:
- 14: Howrah Junction
- 22: Mumbai CSMT
- 23: Mumbai LTT
- 25: Nagpur Junction
- 27: Pune Junction
- 30: Ranchi Junction

See full list when running the application.

## Common Use Cases

### Finding a Direct Train
Best for: Well-connected routes
```python
from route_finder import TrainRouteFinder
finder = TrainRouteFinder()
routes = finder.find_direct_trains('Pune Junction', 'Ranchi Junction')
```

### Finding Any Route (Direct + Multi-hop)
Best for: Any journey
```python
routes = finder.find_all_routes('Pune Junction', 'Ranchi Junction')
# Returns all options sorted by duration
```

### Custom Constraints
```python
routes = finder.find_all_routes(
    'Pune Junction', 
    'Ranchi Junction',
    max_waiting_hours=2,  # Stricter waiting time
    max_hops=2            # Fewer connections
)
```

## Troubleshooting

### "FileNotFoundError: train_timetables.json"
**Solution**: Run `python3 generate_sample_timetables.py`

### "No routes found"
**Possible causes**:
- Stations not connected in sample data
- Spelling mismatch (use station numbers instead)
- Try with different stations from the list

### Want Real Data?
Run the extraction script (takes several hours):
```bash
python3 extract_timetables.py
```

## Next Steps

1. ✅ Use the application with sample data
2. ⏸️ Extract real timetable data for all trains
3. ⏸️ Integrate into web application
4. ⏸️ Add real-time status updates

## Need Help?

- Read: `README.md` for detailed documentation
- Read: `ALGORITHM.md` for technical details
- Read: `IMPLEMENTATION_SUMMARY.md` for overview
- Check: `example_usage.py` for code examples
- Run: `test_route_finder.py` to verify installation

Happy Journey Planning! 🚂
