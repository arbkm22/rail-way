#!/bin/bash
# Demo script to showcase the route finder

echo "================================================================================"
echo "INDIAN RAILWAYS ROUTE FINDER - DEMONSTRATION"
echo "================================================================================"
echo ""
echo "This demonstration shows how to find train routes from Pune to Ranchi"
echo ""
echo "Running: python3 route_finder.py"
echo ""
echo "Input: Pune Junction (station 27)"
echo "Input: Ranchi Junction (station 30)"
echo ""
echo "================================================================================"
echo ""

# Run the route finder with predefined input
echo -e "27\n30" | python3 route_finder.py | head -100

echo ""
echo "================================================================================"
echo "DEMONSTRATION COMPLETE"
echo "================================================================================"
echo ""
echo "The application found multiple routes including:"
echo "  • Direct trains (Pune Hatia SF Express)"
echo "  • Multi-hop connections with timing constraints"
echo ""
echo "For more information, see README.md and ALGORITHM.md"
echo "================================================================================"
