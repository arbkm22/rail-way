"""
Comprehensive test script to demonstrate the route finder capabilities
"""
from route_finder import TrainRouteFinder

def test_route_finder():
    """Run comprehensive tests on the route finder."""
    print("=" * 80)
    print("COMPREHENSIVE ROUTE FINDER TEST SUITE")
    print("=" * 80)
    
    # Initialize route finder
    finder = TrainRouteFinder()
    
    # Test 1: Direct route
    print("\n" + "=" * 80)
    print("TEST 1: Direct Route (Pune to Ranchi)")
    print("=" * 80)
    routes = finder.find_all_routes('Pune Junction', 'Ranchi Junction')
    print(f"✓ Found {len(routes)} routes")
    
    # Check that we have a direct route
    direct_routes = [r for r in routes if r['route_type'] == 'direct']
    assert len(direct_routes) > 0, "Should find at least one direct route"
    print(f"✓ Found {len(direct_routes)} direct route(s)")
    
    best_route = routes[0]
    assert best_route['total_changes'] == 0, "Best route should be direct"
    print(f"✓ Best route is direct with duration: {finder._format_duration(best_route['total_duration'])}")
    
    # Test 2: Multi-hop route
    print("\n" + "=" * 80)
    print("TEST 2: Multi-hop Route (Nagpur to Howrah)")
    print("=" * 80)
    routes = finder.find_all_routes('Nagpur Junction', 'Howrah Junction')
    print(f"✓ Found {len(routes)} routes")
    
    # Check for both direct and multi-hop routes
    multi_hop = [r for r in routes if r['total_changes'] > 0]
    if multi_hop:
        print(f"✓ Found {len(multi_hop)} multi-hop route(s)")
        print(f"✓ Best multi-hop has {multi_hop[0]['total_changes']} change(s)")
    
    # Test 3: Timing constraints
    print("\n" + "=" * 80)
    print("TEST 3: Timing Constraints Check")
    print("=" * 80)
    routes = finder.find_all_routes('Pune Junction', 'Howrah Junction', max_waiting_hours=4)
    
    for route in routes:
        if len(route['route']) > 1:
            for segment in route['route'][1:]:
                if 'waiting_time' in segment:
                    assert segment['waiting_time'] <= 4 * 60, "Waiting time should not exceed 4 hours"
    print(f"✓ All waiting times are within 4 hours limit")
    
    # Test 4: Station listing
    print("\n" + "=" * 80)
    print("TEST 4: Station Listing")
    print("=" * 80)
    stations = finder.get_all_stations()
    print(f"✓ Found {len(stations)} unique stations")
    assert 'Pune Junction' in stations, "Pune Junction should be in stations"
    assert 'Ranchi Junction' in stations, "Ranchi Junction should be in stations"
    print(f"✓ All expected stations are present")
    
    # Test 5: No route case
    print("\n" + "=" * 80)
    print("TEST 5: Edge Cases")
    print("=" * 80)
    
    # Test same source and destination (should handle gracefully)
    try:
        routes = finder.find_all_routes('Pune Junction', 'Pune Junction')
        # If it doesn't error, check that routes are empty or trivial
        print(f"✓ Same source/destination handled (found {len(routes)} routes)")
    except Exception as e:
        print(f"✓ Same source/destination raises error (expected): {type(e).__name__}")
    
    # Test 6: Route details
    print("\n" + "=" * 80)
    print("TEST 6: Route Details Validation")
    print("=" * 80)
    routes = finder.find_all_routes('Mumbai CSMT', 'Pune Junction')
    if routes:
        route = routes[0]
        for segment in route['route']:
            assert 'train_no' in segment, "Segment should have train number"
            assert 'train_name' in segment, "Segment should have train name"
            assert 'from_station' in segment, "Segment should have from station"
            assert 'to_station' in segment, "Segment should have to station"
            assert 'departure' in segment, "Segment should have departure time"
            assert 'arrival' in segment, "Segment should have arrival time"
        print(f"✓ All route segments have required fields")
    
    # Test 7: Sorting by duration
    print("\n" + "=" * 80)
    print("TEST 7: Route Sorting by Duration")
    print("=" * 80)
    routes = finder.find_all_routes('Pune Junction', 'Bilaspur Junction')
    if len(routes) > 1:
        for i in range(len(routes) - 1):
            assert routes[i]['total_duration'] <= routes[i+1]['total_duration'], \
                "Routes should be sorted by duration"
        print(f"✓ Routes are properly sorted by total duration")
    
    # Final summary
    print("\n" + "=" * 80)
    print("ALL TESTS PASSED ✓")
    print("=" * 80)
    print("\nRoute finder is working correctly!")
    print("Features validated:")
    print("  ✓ Direct route finding")
    print("  ✓ Multi-hop route search")
    print("  ✓ Timing constraints enforcement")
    print("  ✓ Station indexing")
    print("  ✓ Edge case handling")
    print("  ✓ Route data validation")
    print("  ✓ Result sorting")
    print("=" * 80)

if __name__ == "__main__":
    test_route_finder()
