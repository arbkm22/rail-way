# Legacy Python Backend Files

This directory contains the legacy Flask-based backend that has been replaced by Next.js API routes.

## Contents

- `api.py` - Flask REST API server (deprecated)
- `app.py` - Flask web application with Jinja templates (deprecated)
- `requirements.txt` - Python dependencies (deprecated)
- `templates/` - HTML templates for Flask app (deprecated)
- `static/` - Static assets for Flask app (deprecated)

## Why These Are Deprecated

The application has been migrated to use Next.js API routes instead of Flask for several reasons:

1. **Simpler Deployment**: No need to manage separate frontend and backend servers
2. **Better Next.js Integration**: API routes are co-located with the frontend
3. **Serverless Ready**: Can be deployed to Vercel, Netlify, etc. without additional configuration
4. **No Python Required**: The entire route-finding logic has been ported to TypeScript
5. **Type Safety**: Full TypeScript support across the entire stack

## Migration Summary

The route-finding algorithm in `route_finder.py` has been ported to TypeScript and can be found at:
- `frontend/lib/routeFinder.ts` - Core route finding logic
- `frontend/app/api/stations/route.ts` - Stations API endpoint
- `frontend/app/api/routes/find/route.ts` - Route finding API endpoint

The Flask API endpoints have been replaced with Next.js API routes that provide the same functionality.

## If You Want to Use the Legacy Backend

If for some reason you need to use the legacy Flask backend:

1. Install dependencies:
   ```bash
   pip install -r legacy/requirements.txt
   ```

2. Run the Flask API:
   ```bash
   python3 legacy/api.py
   ```

3. Update the frontend API client to point to `http://localhost:5001` instead of `/api`

However, this is **not recommended** as the new Next.js-based architecture is simpler and more maintainable.
