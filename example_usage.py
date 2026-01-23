"""
Example usage of the route finder programmatically
"""
from route_finder import TrainRouteFinder

# Initialize route finder
finder = TrainRouteFinder()

# Example 1: Find routes from Pune to Ranchi
print("=" * 80)
print("Example 1: Pune to Ranchi")
print("=" * 80)
routes = finder.find_all_routes('Pune Junction', 'Ranchi Junction', max_waiting_hours=4, max_hops=3)

if routes:
    print(f"\nFound {len(routes)} routes\n")
    # Show top 3 routes
    for i, route in enumerate(routes[:3], 1):
        print(f"Route {i}:")
        finder.print_route(route)

# Example 2: Find routes from Nagpur to Howrah
print("\n" + "=" * 80)
print("Example 2: Nagpur to Howrah")
print("=" * 80)
routes = finder.find_all_routes('Nagpur Junction', 'Howrah Junction', max_waiting_hours=4, max_hops=3)

if routes:
    print(f"\nFound {len(routes)} routes\n")
    # Show top 2 routes
    for i, route in enumerate(routes[:2], 1):
        print(f"Route {i}:")
        finder.print_route(route)
