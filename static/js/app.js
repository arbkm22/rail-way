// Main Application JavaScript
let map;
let markers = [];
let routeLines = [];
let currentRoute = null;

// Initialize map
function initMap() {
    // Create map centered on India
    map = L.map('map').setView([20.5937, 78.9629], 5);

    // Add tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 18,
        minZoom: 4
    }).addTo(map);

    // Add India boundary marker
    const indiaMarker = L.circleMarker([20.5937, 78.9629], {
        radius: 0,
        opacity: 0
    }).addTo(map);
}

// Clear map markers and lines
function clearMap() {
    markers.forEach(marker => map.removeLayer(marker));
    routeLines.forEach(line => map.removeLayer(line));
    markers = [];
    routeLines = [];
}

// Add marker to map
function addStationMarker(stationName, type = 'station') {
    const coords = getStationCoordinates(stationName);
    if (!coords) return null;

    const iconColors = {
        'departure': '#10b981',
        'destination': '#ef4444',
        'transfer': '#f59e0b',
        'station': '#6366f1'
    };

    const iconHtml = type === 'departure' 
        ? '<i class="fas fa-circle-dot"></i>'
        : type === 'destination'
        ? '<i class="fas fa-location-dot"></i>'
        : type === 'transfer'
        ? '<i class="fas fa-exchange-alt"></i>'
        : '<i class="fas fa-circle"></i>';

    const icon = L.divIcon({
        className: 'custom-marker',
        html: `<div class="marker-pin marker-${type}" style="background-color: ${iconColors[type]}">${iconHtml}</div>`,
        iconSize: [40, 40],
        iconAnchor: [20, 40]
    });

    const marker = L.marker(coords, { icon: icon })
        .bindPopup(`<strong>${stationName}</strong><br>${type.charAt(0).toUpperCase() + type.slice(1)}`)
        .addTo(map);

    markers.push(marker);
    return marker;
}

// Draw route on map
function drawRoute(routeData) {
    clearMap();
    
    if (!routeData || !routeData.segments || routeData.segments.length === 0) {
        return;
    }

    const allStations = new Set();
    const transferPoints = new Set();
    
    // Identify all stations and transfer points
    routeData.segments.forEach((segment, index) => {
        allStations.add(segment.from_station);
        allStations.add(segment.to_station);
        
        // Mark intermediate stations as transfer points
        if (index > 0) {
            transferPoints.add(segment.from_station);
        }
    });

    const firstSegment = routeData.segments[0];
    const lastSegment = routeData.segments[routeData.segments.length - 1];
    
    // Add departure marker
    addStationMarker(firstSegment.from_station, 'departure');
    
    // Add destination marker
    addStationMarker(lastSegment.to_station, 'destination');
    
    // Add transfer point markers
    transferPoints.forEach(station => {
        if (station !== firstSegment.from_station && station !== lastSegment.to_station) {
            addStationMarker(station, 'transfer');
        }
    });

    // Draw route lines
    routeData.segments.forEach((segment, index) => {
        const fromCoords = getStationCoordinates(segment.from_station);
        const toCoords = getStationCoordinates(segment.to_station);
        
        if (fromCoords && toCoords) {
            const colors = ['#6366f1', '#8b5cf6', '#ec4899', '#f59e0b'];
            const color = colors[index % colors.length];
            
            const line = L.polyline([fromCoords, toCoords], {
                color: color,
                weight: 4,
                opacity: 0.7,
                dashArray: segment.waiting_time ? '10, 5' : null
            }).addTo(map);
            
            routeLines.push(line);
            
            // Add segment info popup in the middle of the line
            const midLat = (fromCoords[0] + toCoords[0]) / 2;
            const midLng = (fromCoords[1] + toCoords[1]) / 2;
            
            const popup = L.popup()
                .setLatLng([midLat, midLng])
                .setContent(`
                    <div class="route-popup">
                        <strong>${segment.train_name}</strong><br>
                        Train ${segment.train_no}<br>
                        Duration: ${segment.duration}
                        ${segment.waiting_time ? `<br>Waiting: ${segment.waiting_time}` : ''}
                    </div>
                `);
            
            line.bindPopup(popup);
        }
    });

    // Fit map to show all markers
    if (markers.length > 0) {
        const group = L.featureGroup(markers);
        map.fitBounds(group.getBounds().pad(0.1));
    }

    // Show legend
    document.getElementById('map-legend').style.display = 'block';
}

// Form submission handler
document.getElementById('route-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const fromStation = document.getElementById('from_station').value;
    const toStation = document.getElementById('to_station').value;
    const maxWaitingHours = document.getElementById('max_waiting_hours').value;
    const maxHops = document.getElementById('max_hops').value;

    if (!fromStation || !toStation) {
        showNotification('Please select both stations', 'error');
        return;
    }

    if (fromStation === toStation) {
        showNotification('Source and destination cannot be the same', 'error');
        return;
    }

    // Show loading
    document.getElementById('loading').style.display = 'flex';
    document.getElementById('results').innerHTML = '';
    document.getElementById('results-summary').style.display = 'none';

    try {
        const response = await fetch('/find_routes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                from_station: fromStation,
                to_station: toStation,
                max_waiting_hours: maxWaitingHours,
                max_hops: maxHops
            })
        });

        const data = await response.json();

        // Hide loading
        document.getElementById('loading').style.display = 'none';

        if (data.error) {
            showNotification(data.error, 'error');
            return;
        }

        if (data.routes.length === 0) {
            document.getElementById('results').innerHTML = `
                <div class="no-results">
                    <i class="fas fa-search"></i>
                    <h3>No Routes Found</h3>
                    <p>${data.message || 'Try adjusting your search parameters'}</p>
                </div>
            `;
            return;
        }

        // Display results summary
        displayResultsSummary(data);

        // Display routes
        displayRoutes(data);

        // Draw first route on map
        if (data.routes.length > 0) {
            drawRoute(data.routes[0]);
            currentRoute = data.routes;
        }

        // Scroll to results
        document.getElementById('results').scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    } catch (error) {
        document.getElementById('loading').style.display = 'none';
        showNotification('Failed to fetch routes: ' + error.message, 'error');
    }
});

// Display results summary
function displayResultsSummary(data) {
    const summary = document.getElementById('results-summary');
    summary.innerHTML = `
        <div class="summary-content">
            <div class="summary-icon">
                <i class="fas fa-check-circle"></i>
            </div>
            <div class="summary-text">
                <strong>${data.routes.length} route(s) found</strong>
                <p>From <strong>${data.from_station}</strong> to <strong>${data.to_station}</strong></p>
            </div>
        </div>
    `;
    summary.style.display = 'block';
}

// Display routes
function displayRoutes(data) {
    let html = '';

    data.routes.forEach((route, index) => {
        const isDirectRoute = route.num_changes === 0;
        
        html += `
            <div class="route-card" data-route-index="${index}">
                <div class="route-card-header">
                    <div class="route-number">
                        <span class="route-badge">${index + 1}</span>
                    </div>
                    <div class="route-summary">
                        <div class="route-title">
                            <span class="route-type-badge ${isDirectRoute ? 'direct' : 'connecting'}">
                                <i class="fas ${isDirectRoute ? 'fa-arrow-right' : 'fa-code-branch'}"></i>
                                ${isDirectRoute ? 'Direct' : route.num_changes + ' Change' + (route.num_changes > 1 ? 's' : '')}
                            </span>
                        </div>
                        <div class="route-metrics">
                            <div class="metric">
                                <i class="fas fa-clock"></i>
                                <span>${route.total_duration}</span>
                            </div>
                        </div>
                    </div>
                    <button class="view-on-map-btn" onclick="viewRouteOnMap(${index})">
                        <i class="fas fa-map-marked-alt"></i>
                        View on Map
                    </button>
                </div>
                <div class="route-segments">
        `;

        route.segments.forEach((segment, segIndex) => {
            html += `
                <div class="segment-card">
                    <div class="segment-timeline">
                        <div class="timeline-dot ${segIndex === 0 ? 'start' : ''}"></div>
                        <div class="timeline-line"></div>
                    </div>
                    <div class="segment-content">
                        <div class="train-info">
                            <i class="fas fa-train"></i>
                            <strong>${segment.train_name}</strong>
                            <span class="train-number">#${segment.train_no}</span>
                        </div>
                        <div class="journey-details">
                            <div class="station-info departure-info">
                                <div class="station-name">
                                    <i class="fas fa-circle-dot"></i>
                                    ${segment.from_station}
                                </div>
                                <div class="time-info">
                                    <span class="time">${segment.departure}</span>
                                    <span class="label">Departure</span>
                                </div>
                            </div>
                            <div class="duration-info">
                                <i class="fas fa-arrow-down"></i>
                                <span>${segment.duration}</span>
                            </div>
                            <div class="station-info arrival-info">
                                <div class="station-name">
                                    <i class="fas fa-location-dot"></i>
                                    ${segment.to_station}
                                </div>
                                <div class="time-info">
                                    <span class="time">${segment.arrival}</span>
                                    <span class="label">Arrival</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            if (segment.waiting_time && segIndex < route.segments.length - 1) {
                html += `
                    <div class="waiting-info">
                        <i class="fas fa-hourglass-half"></i>
                        <span>Waiting time at ${segment.to_station}: <strong>${segment.waiting_time}</strong></span>
                    </div>
                `;
            }
        });

        html += `
                </div>
            </div>
        `;
    });

    document.getElementById('results').innerHTML = html;
}

// View specific route on map
function viewRouteOnMap(routeIndex) {
    if (currentRoute && currentRoute[routeIndex]) {
        drawRoute(currentRoute[routeIndex]);
        // Scroll to map
        document.getElementById('map').scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Highlight selected route
        document.querySelectorAll('.route-card').forEach((card, index) => {
            card.classList.toggle('highlighted', index === routeIndex);
        });
    }
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element if it doesn't exist
    let notification = document.getElementById('notification');
    if (!notification) {
        notification = document.createElement('div');
        notification.id = 'notification';
        notification.className = 'notification';
        document.body.appendChild(notification);
    }

    notification.className = `notification ${type} show`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'error' ? 'exclamation-circle' : type === 'success' ? 'check-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;

    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

// Swap stations button
document.getElementById('swap-stations').addEventListener('click', function() {
    const fromSelect = document.getElementById('from_station');
    const toSelect = document.getElementById('to_station');
    
    const temp = fromSelect.value;
    fromSelect.value = toSelect.value;
    toSelect.value = temp;
    
    // Add animation
    this.style.transform = 'rotate(180deg)';
    setTimeout(() => {
        this.style.transform = 'rotate(0deg)';
    }, 300);
});

// Advanced options toggle
document.getElementById('advanced-toggle').addEventListener('click', function() {
    const content = document.getElementById('advanced-content');
    const isOpen = content.style.maxHeight;
    
    if (isOpen) {
        content.style.maxHeight = null;
        this.classList.remove('open');
    } else {
        content.style.maxHeight = content.scrollHeight + 'px';
        this.classList.add('open');
    }
});

// Reset map button
document.getElementById('reset-map').addEventListener('click', function() {
    map.setView([20.5937, 78.9629], 5);
    clearMap();
    document.getElementById('map-legend').style.display = 'none';
});

// Initialize map when page loads
document.addEventListener('DOMContentLoaded', function() {
    initMap();
});
