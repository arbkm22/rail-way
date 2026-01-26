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
        
        // India bounds (approximate)
        const bounds = {
            minLat: 8,
            maxLat: 35,
            minLng: 68,
            maxLng: 97
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
        
        // Draw India map background
        function drawIndiaOutline() {
            // Simplified India shape
            ctx.fillStyle = '#e0f2fe';
            ctx.strokeStyle = '#0284c7';
            ctx.lineWidth = 2;
            
            // Draw a simplified polygon representing India
            const indiaShape = [
                [35, 75], [32, 78], [30, 88], [28, 92], [25, 88],
                [22, 88], [20, 85], [18, 77], [16, 75], [12, 77],
                [10, 77], [8, 75], [8, 72], [10, 70], [15, 68],
                [20, 70], [24, 70], [28, 72], [30, 70], [33, 72], [35, 75]
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
        }
        
        // Draw the map
        function render() {
            // Clear canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Draw background
            ctx.fillStyle = '#f0f9ff';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw India outline
            drawIndiaOutline();
            
            // Draw grid
            ctx.strokeStyle = '#bae6fd';
            ctx.lineWidth = 1;
            ctx.setLineDash([5, 5]);
            for (let i = 1; i < 10; i++) {
                const x = (canvas.width / 10) * i;
                const y = (canvas.height / 10) * i;
                ctx.beginPath();
                ctx.moveTo(x, 0);
                ctx.lineTo(x, canvas.height);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(0, y);
                ctx.lineTo(canvas.width, y);
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
