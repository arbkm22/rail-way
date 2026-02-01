# GitHub Copilot Instructions for Indian Railways Route Finder

## Project Overview

This is a modern train route finder application for Indian Railways built with Next.js and TypeScript. The application allows users to find direct and multi-hop train routes between stations with interactive map visualizations.

**Key Features:**
- Direct and multi-hop route finding between railway stations
- Interactive Leaflet maps with OpenStreetMap tiles
- Serverless architecture using Next.js API routes
- Mobile-responsive design
- No paid services - completely open source

## Technology Stack

### Frontend
- **Framework:** Next.js 16 (App Router)
- **UI Library:** React 19
- **Language:** TypeScript 5 (strict mode)
- **Styling:** Tailwind CSS 4
- **Maps:** Leaflet.js with React-Leaflet
- **Map Tiles:** OpenStreetMap (free)

### Backend
- **API:** Next.js API Routes (serverless)
- **Runtime:** Node.js 20+
- **Data Format:** JSON, GeoJSON

### Python Utilities (Legacy/Tools)
- **Language:** Python 3.8+
- **Web Scraping:** Selenium, BeautifulSoup
- **Data Processing:** JSON manipulation
- **Purpose:** Data extraction and utility scripts (not required for main app)

## Code Style and Conventions

### TypeScript/React

#### General Guidelines
- Use **strict TypeScript** with all type checking enabled
- Prefer **functional components** with hooks over class components
- Use **named exports** for components and utilities
- Use **PascalCase** for React components and TypeScript types/interfaces
- Use **camelCase** for variables, functions, and file names (except components)
- Use **snake_case** for JSON data keys to match API responses

#### React Patterns
- Always mark client components with `'use client'` directive at the top
- Use **React hooks** (useState, useEffect, useRef, etc.) for state management
- Prefer **composition over inheritance**
- Keep components focused and single-responsibility
- Use proper cleanup in useEffect hooks (return cleanup functions)

#### TypeScript Best Practices
- Define **explicit interfaces** for all data structures
- Use **type annotations** for function parameters and return types
- Avoid `any` type - use proper types or `unknown` if necessary
- Use **optional chaining** (`?.`) and **nullish coalescing** (`??`) operators
- Define data models in separate interface files when shared across components

#### File Organization
```
frontend/
├── app/              # Next.js App Router pages
│   ├── api/         # API route handlers
│   ├── layout.tsx   # Root layout
│   └── page.tsx     # Page components
├── components/       # Reusable React components
├── lib/             # Utility functions and business logic
└── public/          # Static assets
```

#### Imports
- Use path alias `@/` for imports (e.g., `import { api } from '@/lib/api'`)
- Group imports: React/Next.js first, then third-party, then local
- Sort imports alphabetically within groups

### Python

#### Style Guidelines
- Follow **PEP 8** style guide
- Use **snake_case** for functions and variables
- Use **docstrings** for all functions and classes
- Use **type hints** where applicable
- Prefer **f-strings** for string formatting

#### Module Patterns
- Keep utility scripts self-contained
- Use `if __name__ == "__main__":` for executable scripts
- Add comprehensive error handling with try/except blocks
- Include progress logging for long-running operations

## API and Data Formats

### JSON Structure
- Use **snake_case** for JSON keys (e.g., `train_no`, `station_name`)
- Keep data structures consistent with existing `train_timetables.json` format
- Use **GeoJSON** standard for geographical data (`[longitude, latitude]` order)

### API Routes
- Use Next.js API route handlers in `app/api/` directory
- Return proper HTTP status codes
- Include error handling and validation
- Return JSON responses with appropriate headers
- Support CORS if needed for external access

### Example Train Data Structure
```typescript
{
  "trainNo": number,
  "trainName": string,
  "fromStation": string,
  "toStation": string,
  "timetable": [
    {
      "station_code": string,
      "station_name": string,
      "arrival_time": string,
      "departure_time": string,
      "distance_km": string
    }
  ]
}
```

## Map and Geospatial

### Leaflet Integration
- Use dynamic imports to avoid SSR issues: `const Map = dynamic(() => import('@/components/Map'), { ssr: false })`
- Fix default marker icons for Next.js environment
- Use **GeoJSON** format for all geographical data
- Coordinate order: **[longitude, latitude]** (GeoJSON standard)

### Map Features
- Initialize map centered on India: `[20.5937, 78.9629]`
- Use OpenStreetMap tiles (no API key required)
- Color code markers:
  - 🟢 Green: Departure station
  - 🔴 Red: Destination station
  - 🟠 Orange: Transfer/intermediate stations
- Include proper cleanup in useEffect to prevent memory leaks

## Security Practices

### General Security
- **Never commit** API keys, secrets, or credentials
- Use environment variables for configuration (`.env.local`)
- Validate and sanitize all user inputs
- Use TypeScript's type system to prevent runtime errors

### Data Handling
- Validate station names against known station list
- Sanitize search parameters before processing
- Use proper error boundaries in React components
- Handle edge cases (missing data, invalid times, etc.)

## Testing and Validation

### Testing Approach
- Test Python utilities with existing test files (e.g., `test_route_finder.py`)
- Validate routes against realistic scenarios
- Test edge cases: same station, non-existent stations, timing conflicts
- Verify map rendering and interaction

### Development Workflow
```bash
# Frontend development
cd frontend
npm install
npm run dev          # Start dev server on localhost:3000
npm run build        # Build for production
npm run lint         # Run ESLint

# Python utilities (optional)
python3 generate_sample_timetables.py  # Generate test data
python3 test_route_finder.py           # Run route finder tests
```

## Documentation

### Code Comments
- Add **JSDoc comments** for public functions and complex logic
- Use inline comments sparingly - prefer self-documenting code
- Document **why** not **what** when adding comments
- Keep comments up-to-date with code changes

### README Files
- Update README.md when adding major features
- Keep QUICKSTART.md concise and actionable
- Document API endpoints in ARCHITECTURE.md
- Include examples for complex features

## Performance Considerations

### Frontend Optimization
- Use **dynamic imports** for heavy components (e.g., Leaflet maps)
- Minimize bundle size - avoid unnecessary dependencies
- Use **React.memo** for expensive component re-renders
- Optimize images and assets
- Lazy load routes/components when possible

### Algorithm Efficiency
- Route finding algorithm uses BFS (Breadth-First Search)
- Build station index once at initialization
- Limit search depth with `max_hops` parameter
- Use early termination when possible

## Route Finding Logic

### Key Algorithms
- **Direct Route Finding:** Check if any train directly connects two stations
- **Multi-hop Routes:** BFS algorithm to find connections with train changes
- **Timing Validation:** Ensure waiting times don't exceed `max_waiting_hours` (default: 4 hours)
- **No Circular Routes:** Track visited stations to avoid loops

### Time Handling
- Times in HH:MM format (24-hour)
- Handle day crossovers (e.g., depart 23:00, arrive 02:00 next day)
- "Source" means arrival time not applicable
- "Destination" means departure time not applicable

## Common Tasks

### Adding a New Feature
1. Plan the minimal change needed
2. Update TypeScript types/interfaces if needed
3. Implement in appropriate location (component, lib, API route)
4. Test the feature locally
5. Update documentation if it affects user-facing functionality

### Fixing a Bug
1. Reproduce the issue locally
2. Identify root cause
3. Make minimal fix
4. Test the fix
5. Consider edge cases

### Adding New Data
1. Follow existing JSON structure in `train_timetables.json`
2. Validate data format (station names, times, coordinates)
3. Ensure GeoJSON uses `[longitude, latitude]` order
4. Update sample data if needed for testing

## Dependencies

### When Adding Dependencies
- Check if functionality exists in current stack
- Prefer lightweight, well-maintained packages
- Avoid packages with security vulnerabilities
- Update package.json with specific version ranges
- Run `npm install` and verify the app still works

### Approved Libraries
- **DO USE:** React, Next.js, Leaflet, Tailwind CSS (already included)
- **AVOID:** jQuery, Bootstrap, unnecessary UI frameworks
- **CONSIDER:** Only add if solving a specific problem that can't be solved with existing tools

## Architecture Notes

### Current vs Legacy
- **Current:** Next.js app with API routes (frontend directory)
- **Legacy:** Python Flask app (legacy directory) - kept for reference only
- Main app is **fully TypeScript** - no Python backend required
- Python scripts are **utilities only** for data extraction

### Data Flow
1. User selects stations in UI (React component)
2. Request sent to Next.js API route (`/api/routes/find`)
3. TypeScript route finder algorithm processes request
4. Results returned as JSON with GeoJSON geometry
5. Map component visualizes routes on Leaflet map

## Restrictions

### Do Not
- Do not modify legacy Python code unless specifically updating utilities
- Do not add Python backend dependencies to main app
- Do not use paid services or API keys for core functionality
- Do not break existing API contracts without version increment
- Do not commit `node_modules/`, `.next/`, or build artifacts
- Do not use inline styles - use Tailwind CSS classes
- Do not use `any` type in TypeScript - use proper types

### Do
- Do keep changes minimal and focused
- Do maintain backward compatibility with existing data
- Do use TypeScript strict mode
- Do validate all inputs
- Do clean up resources in useEffect hooks
- Do use semantic HTML elements
- Do make components reusable and composable

## Questions or Clarifications

If you're unsure about:
- **Code style:** Refer to existing code in the same module
- **Data structure:** Check `train_timetables.json` and type definitions
- **API format:** See `frontend/app/api/` route handlers
- **Map integration:** Review `frontend/components/Map.tsx`
- **Route algorithm:** Study `frontend/lib/routeFinder.ts`

---

**Remember:** The goal is to help users find train routes efficiently with a clean, fast, and reliable interface. Keep the user experience simple and intuitive!
