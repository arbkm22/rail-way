// Custom lightweight map implementation for Indian Railways
const L = {
    map: function(id) {
        const container = document.getElementById(id);
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        // Set canvas size
        canvas.width = container.clientWidth;
        canvas.height = container.clientHeight;
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        container.appendChild(canvas);
        
        // India bounds (actual geographic bounds)
        const bounds = {
            minLat: 6.5,
            maxLat: 37,
            minLng: 68,
            maxLng: 98
        };
        
        let markers = [];
        let lines = [];
        let currentView = { lat: 20.5937, lng: 78.9629, zoom: 1 };
        
        // Convert lat/lng to canvas coordinates
        function project(lat, lng) {
            const x = ((lng - bounds.minLng) / (bounds.maxLng - bounds.minLng)) * canvas.width;
            const y = ((bounds.maxLat - lat) / (bounds.maxLat - bounds.minLat)) * canvas.height;
            return { x, y };
        }
        
        // Draw India map background with accurate outline
        function drawIndiaOutline() {
            ctx.fillStyle = '#e0f2fe';
            ctx.strokeStyle = '#0369a1';
            ctx.lineWidth = 2;
            
            // More accurate India shape coordinates (simplified but recognizable)
            const indiaShape = [
                // Kashmir and North
                [35.5, 74], [35, 75], [34.5, 76], [34, 77], [33.5, 78],
                [33, 78.5], [32.5, 79], [32, 79.5], [31.5, 80],
                // Northeast border
                [30.5, 81], [30, 82], [29, 84], [28, 86], [27.5, 88],
                [27, 89], [26.5, 90], [26, 91], [25.5, 92],
                // Northeast tip (Arunachal)
                [28, 94], [27.5, 95.5], [27, 96.5], [26.5, 97],
                // Down to Myanmar border
                [26, 97], [25, 96.5], [24, 95], [23, 93.5], [22, 92.5],
                // Bangladesh border and east coast
                [21.5, 91.5], [21, 90], [20.5, 88.5], [20, 87.5],
                // Bay of Bengal coast
                [19, 85], [18, 84], [17, 83], [16, 82.5], [15, 81.5],
                [14, 81], [13, 80.5], [12, 80.2], [11, 80],
                // South tip
                [10, 79.5], [9, 78.5], [8.5, 78], [8, 77.5],
                // West coast going up
                [8, 76.5], [9, 76], [10, 75.5], [11, 75.5], [12, 75],
                [13, 74.5], [14, 74.5], [15, 74], [16, 73.5], [17, 73],
                [18, 73], [19, 73], [20, 72.5], [21, 72], [22, 71.5],
                [23, 70.5], [24, 70], [25, 70], [26, 70], [27, 70],
                // Gujarat coast
                [22, 69], [21.5, 68.5], [21, 68], [22, 68.5], [23, 68.5],
                // Back to Rajasthan and up to Kashmir
                [24, 69], [25, 70], [26, 70.5], [27, 71], [28, 71.5],
                [29, 72], [30, 73], [31, 74], [32, 74.5], [33, 74.5],
                [34, 74.5], [35.5, 74]
            ];
            
            ctx.beginPath();
            indiaShape.forEach((point, i) => {
                const pos = project(point[0], point[1]);
                if (i === 0) ctx.moveTo(pos.x, pos.y);
                else ctx.lineTo(pos.x, pos.y);
            });
            ctx.closePath();
            ctx.fill();
            ctx.stroke();
            
            // Add some major cities as reference points (light gray dots)
            const majorCities = [
                [28.7, 77.2],   // Delhi
                [19.08, 72.88], // Mumbai
                [13.08, 80.27], // Chennai
                [22.57, 88.36], // Kolkata
                [12.97, 77.59], // Bangalore
                [17.38, 78.48]  // Hyderabad
            ];
            
            ctx.fillStyle = '#cbd5e1';
            majorCities.forEach(city => {
                const pos = project(city[0], city[1]);
                ctx.beginPath();
                ctx.arc(pos.x, pos.y, 3, 0, Math.PI * 2);
                ctx.fill();
            });
        }
        
        // Draw the map
        function render() {
            // Clear canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Draw ocean/background
            ctx.fillStyle = '#dbeafe';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw India outline
            drawIndiaOutline();
            
            // Draw subtle latitude/longitude reference lines
            ctx.strokeStyle = 'rgba(186, 230, 253, 0.5)';
            ctx.lineWidth = 0.5;
            ctx.setLineDash([3, 3]);
            
            // Draw latitude lines every 5 degrees
            for (let lat = 10; lat <= 35; lat += 5) {
                const points = [];
                for (let lng = bounds.minLng; lng <= bounds.maxLng; lng += 0.5) {
                    points.push(project(lat, lng));
                }
                ctx.beginPath();
                points.forEach((p, i) => {
                    if (i === 0) ctx.moveTo(p.x, p.y);
                    else ctx.lineTo(p.x, p.y);
                });
                ctx.stroke();
            }
            
            // Draw longitude lines every 5 degrees
            for (let lng = 70; lng <= 95; lng += 5) {
                const points = [];
                for (let lat = bounds.minLat; lat <= bounds.maxLat; lat += 0.5) {
                    points.push(project(lat, lng));
                }
                ctx.beginPath();
                points.forEach((p, i) => {
                    if (i === 0) ctx.moveTo(p.x, p.y);
                    else ctx.lineTo(p.x, p.y);
                });
                ctx.stroke();
            }
            ctx.setLineDash([]);
            
            // Draw lines (routes)
            lines.forEach(line => {
                const from = project(line.coords[0][0], line.coords[0][1]);
                const to = project(line.coords[1][0], line.coords[1][1]);
                
                // Draw shadow
                ctx.strokeStyle = 'rgba(0, 0, 0, 0.1)';
                ctx.lineWidth = (line.weight || 3) + 2;
                ctx.beginPath();
                ctx.moveTo(from.x + 2, from.y + 2);
                ctx.lineTo(to.x + 2, to.y + 2);
                ctx.stroke();
                
                // Draw main line
                ctx.strokeStyle = line.color || '#6366f1';
                ctx.lineWidth = line.weight || 4;
                ctx.setLineDash(line.dashArray || []);
                ctx.globalAlpha = line.opacity || 1;
                
                ctx.beginPath();
                ctx.moveTo(from.x, from.y);
                ctx.lineTo(to.x, to.y);
                ctx.stroke();
                
                ctx.setLineDash([]);
                ctx.globalAlpha = 1;
                
                // Draw arrow
                const angle = Math.atan2(to.y - from.y, to.x - from.x);
                const arrowSize = 12;
                ctx.fillStyle = line.color || '#6366f1';
                ctx.beginPath();
                ctx.moveTo(to.x, to.y);
                ctx.lineTo(
                    to.x - arrowSize * Math.cos(angle - Math.PI / 6),
                    to.y - arrowSize * Math.sin(angle - Math.PI / 6)
                );
                ctx.lineTo(
                    to.x - arrowSize * Math.cos(angle + Math.PI / 6),
                    to.y - arrowSize * Math.sin(angle + Math.PI / 6)
                );
                ctx.closePath();
                ctx.fill();
            });
            
            // Draw markers
            markers.forEach(marker => {
                const pos = project(marker.lat, marker.lng);
                
                // Draw shadow
                ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
                ctx.beginPath();
                ctx.arc(pos.x + 2, pos.y + 2, 10, 0, Math.PI * 2);
                ctx.fill();
                
                // Draw marker circle
                ctx.fillStyle = marker.color || '#6366f1';
                ctx.beginPath();
                ctx.arc(pos.x, pos.y, 10, 0, Math.PI * 2);
                ctx.fill();
                
                // Draw marker border
                ctx.strokeStyle = 'white';
                ctx.lineWidth = 3;
                ctx.stroke();
                
                // Draw inner dot
                ctx.fillStyle = 'white';
                ctx.beginPath();
                ctx.arc(pos.x, pos.y, 4, 0, Math.PI * 2);
                ctx.fill();
                
                // Draw label
                if (marker.label) {
                    ctx.fillStyle = 'white';
                    ctx.fillRect(pos.x - 40, pos.y - 30, 80, 20);
                    ctx.strokeStyle = marker.color || '#6366f1';
                    ctx.lineWidth = 2;
                    ctx.strokeRect(pos.x - 40, pos.y - 30, 80, 20);
                    
                    ctx.fillStyle = '#1f2937';
                    ctx.font = 'bold 11px sans-serif';
                    ctx.textAlign = 'center';
                    ctx.fillText(marker.label, pos.x, pos.y - 16);
                }
            });
        }
        
        // Handle resize
        window.addEventListener('resize', () => {
            canvas.width = container.clientWidth;
            canvas.height = container.clientHeight;
            render();
        });
        
        // Public API
        return {
            setView: function(coords, zoom) {
                currentView = { lat: coords[0], lng: coords[1], zoom: zoom };
                render();
                return this;
            },
            
            marker: function(coords, options) {
                const marker = {
                    lat: coords[0],
                    lng: coords[1],
                    color: options?.icon?.color || '#6366f1',
                    label: options?.label || null,
                    popup: options?.popup || null
                };
                
                markers.push(marker);
                render();
                
                return {
                    bindPopup: function(content) {
                        marker.popup = content;
                        return this;
                    },
                    addTo: function() {
                        return this;
                    }
                };
            },
            
            polyline: function(coords, options) {
                const line = {
                    coords: coords,
                    color: options?.color || '#6366f1',
                    weight: options?.weight || 4,
                    opacity: options?.opacity || 1,
                    dashArray: options?.dashArray || null
                };
                
                lines.push(line);
                render();
                
                return {
                    bindPopup: function(content) {
                        line.popup = content;
                        return this;
                    },
                    addTo: function() {
                        return this;
                    }
                };
            },
            
            removeLayer: function(layer) {
                render();
            },
            
            fitBounds: function(bounds) {
                render();
                return this;
            },
            
            clearMarkers: function() {
                markers = [];
                lines = [];
                render();
            }
        };
    },
    
    tileLayer: function(url, options) {
        return {
            addTo: function(map) {
                return this;
            }
        };
    },
    
    circleMarker: function(coords, options) {
        return {
            addTo: function(map) {
                return this;
            }
        };
    },
    
    divIcon: function(options) {
        return {
            color: options.color || '#6366f1',
            className: options.className
        };
    },
    
    popup: function() {
        return {
            setLatLng: function() { return this; },
            setContent: function() { return this; }
        };
    },
    
    featureGroup: function(layers) {
        return {
            getBounds: function() {
                return {
                    pad: function() {
                        return [[8, 68], [35, 97]];
                    }
                };
            }
        };
    }
};

// Store reference globally
window.L = L;
