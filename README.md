# Mood DJ - Music Mood Analysis App

A Flask web application that analyzes your mood from text and suggests matching music on Spotify.

## Features

- User authentication with login/signup
- Mood analysis using VADER sentiment analysis
- Spotify music recommendations based on mood
- Admin panel for user management
- PostgreSQL database support
- Responsive dark theme with smooth animations

## Setup

### Prerequisites

- Python 3.8+
- PostgreSQL database
- Spotify account (for music links)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd mood-music-app
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL database:
```sql
CREATE DATABASE mood_dj;
CREATE USER mood_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE mood_dj TO mood_user;
```

5. Configure environment variables:
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://mood_user:your_password@localhost:5432/mood_dj
```

6. Initialize the database:
```bash
python init_db.py
```

### Running the Application

```bash
python app.py
```

The app will be available at `http://localhost:5000`

### Default Admin Account

- Username: `admin`
- Password: `admin123`

**Important:** Change the default admin password in production!

## Database Migration

When switching from SQLite to PostgreSQL or updating the schema:

1. The app will automatically create tables on first run
2. For production deployments, consider using Flask-Migrate for proper migrations

## Development

- The app uses SQLite by default if no DATABASE_URL is provided
- Set `DATABASE_URL` environment variable for PostgreSQL
- Debug mode is enabled by default

## Technologies Used

- Flask
- SQLAlchemy
- PostgreSQL
- VADER Sentiment Analysis
- Spotify Web API
- Flask-Login for authentication