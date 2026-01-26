# Legacy Files

This document lists deprecated files that are kept for reference but are no longer part of the recommended architecture.

## Deprecated Web Application

### Files
- `app.py` - Old Flask application with Jinja2 templates
- `templates/index.html` - Old HTML template
- `static/` directory - Old static assets (CSS, JS)
  - `static/css/` - Old stylesheets
  - `static/js/` - Old JavaScript files

### Reason for Deprecation
These files implemented a server-side rendered Flask application with Jinja2 templates. They have been replaced by:
- Modern REST API (`api.py`)
- Next.js frontend (`frontend/`)

### Migration Path
If you're currently using the old application:

1. **Old way** (deprecated):
   ```bash
   python3 app.py
   # Visit http://localhost:5000
   ```

2. **New way** (recommended):
   ```bash
   # Terminal 1: Start API
   python3 api.py
   
   # Terminal 2: Start Frontend
   cd frontend && npm run dev
   # Visit http://localhost:3000
   ```

### Why Keep These Files?
- **Reference**: Developers can see the evolution of the project
- **Comparison**: Understand differences between old and new architecture
- **Learning**: Examples of Flask template rendering vs REST API

### Should I Delete Them?
No immediate need, but they can be removed in a future cleanup if desired. They don't interfere with the new architecture since:
- Old app runs on port 5000
- New API runs on port 5001
- Frontend runs on port 3000

## Still Supported Files

These files are still part of the active system:

### Core Logic
- `route_finder.py` - Route finding algorithm (used by both old and new)
- `train_timetables.json` - Train data (used by both old and new)
- `generate_sample_timetables.py` - Data generator (still useful)

### Utilities
- `extract_timetables.py` - Web scraper for real data
- `test_route_finder.py` - Tests for route finder
- `example_usage.py` - CLI examples

## Future Cleanup

In a future PR, consider:
- Moving legacy files to `legacy/` directory
- Adding clear deprecation warnings in `app.py`
- Creating an upgrade guide for users
