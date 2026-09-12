# Habit-Tracker
A REST API for tracking daily habits and streaks, built with FastAPI and SQLAlchemy

## Features
- Create, list, view and delete habits
- Log habit completions by date
- Automatic streak calculation (consecutive days completed)
- Interactive API documentation via Swagger UI
- Automated test suite using pytest

## Tech Stack
- **Python 3**
- **FastAPI** – web framework
- **SQLAlchemy** – ORM / database layer
- **SQLite** – database
- **Pydantic** – request/response validation
- **pytest** – automated testing

## Setup
 
1. Clone the repository
```
   git clone https://github.com/jdmowatt/Habit-Tracker
   cd habit-tracker
```
 
2. Create and activate a virtual environment
```
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate    # Mac/Linux
```
 
3. Install dependencies
```
   pip install -r requirements.txt
```
 
4. Run the server
```
   uvicorn main:app --reload
```
 
5. Open your browser to `http://127.0.0.1:8000/docs` for interactive API documentation.

## Design Notes
 
- Timestamps are stored in UTC to avoid timezone inconsistencies.
- Streak calculation anchors on today or yesterday, so a streak isn't broken just because today hasn't been logged yet.
- Request/response schemas are kept separate from database models so clients can't set server-controlled fields (like `id` or `created_at`) directly.
## Possible Future Improvements
 
- Update endpoint for renaming habits (currently supports Create/Read/Delete, not Update)
- User accounts / authentication
- Deployment to a live host
