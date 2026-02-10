# Mood DJ - AI-Powered Music Mood Analysis App

A sophisticated Flask web application that uses Groq AI to analyze your mood from text and provides personalized Spotify music recommendations with direct playlist integration.

## Features

### Advanced AI Mood Analysis
- **Groq AI Integration**: Uses Llama 3.3 70B Versatile model for nuanced mood detection
- **Multi-dimensional Analysis**: Detects mood, energy levels, emotions, and confidence scores
- **Smart Keywords**: AI-generated Spotify search keywords optimized for music discovery

### Spotify Integration
- **OAuth Authentication**: Secure connection to Spotify accounts
- **Real-time Search**: Direct API calls to find matching tracks
- **Playlist Management**: Create new playlists or add to existing ones
- **Visual Track Display**: Album art, artist info, and direct play links

### Modern UI/UX
- **Full-Screen Design**: Immersive experience with responsive two-column layout
- **Dark Theme**: Beautiful dark interface with smooth animations
- **Interactive Elements**: Expandable analysis details, modal dialogs
- **Mobile Responsive**: Optimized for all device sizes

### User Management
- **Authentication System**: Secure login/signup with Flask-Login
- **Admin Panel**: User management interface
- **Database Flexibility**: PostgreSQL or SQLite support

## Quick Start

### Prerequisites

- Python 3.8+
- Spotify Developer Account
- Groq API Account

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd mood-music-app
```

2. **Create virtual environment:**
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Get API Credentials:**

   **Spotify API:**
   - Visit [Spotify Developer Dashboard](https://developer.spotify.com/)
   - Create a new app
   - Copy Client ID and Client Secret

   **Groq API:**
   - Visit [Groq Console](https://console.groq.com/)
   - Get your API key

5. **Configure environment variables:**
Create a `.env` file in the root directory:
```env
# Flask Configuration
SECRET_KEY=your-super-secret-key-here-change-this-in-production

# Database Configuration
DATABASE_URL=sqlite:///data.db
# Or for PostgreSQL:
# DATABASE_URL=postgresql://username:password@localhost:5432/database_name

# AI Configuration
GROQ_API_KEY=your-groq-api-key-here

# Spotify Configuration
SPOTIFY_CLIENT_ID=your-spotify-client-id-here
SPOTIFY_CLIENT_SECRET=your-spotify-client-secret-here
```

6. **Initialize the database:**
```bash
python init_db.py
```

7. **Run the application:**
```bash
python app.py
```

Visit `http://localhost:5000` in your browser!

## How It Works

1. **Write Your Mood**: Share how you're feeling in the text area
2. **AI Analysis**: Groq AI analyzes your text for mood, emotions, and energy
3. **Smart Search**: AI generates optimized keywords for Spotify search
4. **Get Recommendations**: View personalized track suggestions with album art
5. **Save to Spotify**: Add tracks directly to your playlists or create new ones

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Flask session secret | Yes |
| `DATABASE_URL` | Database connection string | No (defaults to SQLite) |
| `GROQ_API_KEY` | Groq AI API key | Yes |
| `SPOTIFY_CLIENT_ID` | Spotify app client ID | Yes |
| `SPOTIFY_CLIENT_SECRET` | Spotify app client secret | Yes |

### Database Options

**SQLite (Development):**
```env
DATABASE_URL=sqlite:///data.db
```

**PostgreSQL (Production):**
```env
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

## Default Accounts

### Admin Account
- **Username:** `admin`
- **Password:** `admin123`
- **Email:** `admin@example.com`

**Important:** Change the default admin password in production!

## API Endpoints

### Spotify Integration
- `GET /spotify/login` - Initiate Spotify OAuth
- `GET /spotify/callback` - OAuth callback handler
- `GET /spotify/search?q=<query>` - Search Spotify tracks
- `POST /spotify/create_playlist` - Create new playlist
- `POST /spotify/add_to_playlist` - Add track to playlist
- `GET /spotify/playlists` - Get user's playlists

## UI Features

### Responsive Design
- **Desktop:** Two-column layout (input left, analysis right)
- **Mobile:** Single column with stacked sections
- **Full-screen:** Utilizes entire viewport for immersive experience

### Interactive Elements
- **Expandable Analysis:** Detailed mood breakdown can be toggled
- **Playlist Modal:** Clean interface for playlist selection
- **Track Cards:** Visual track display with add/play buttons
- **Smooth Animations:** CSS transitions throughout

## AI Mood Analysis

The app uses Groq's Llama 3.3 70B Versatile model to analyze text and return:
- **Mood Label**: happy, sad, excited, calm, etc.
- **Energy Level**: high, medium, low
- **Confidence Score**: 0-1 indicating analysis certainty
- **Emotions**: List of detected emotions
- **Example Songs**: AI-suggested track examples
- **Spotify Keywords**: Optimized search terms

## Security Features

- **Secure Authentication**: Flask-Login with password hashing
- **OAuth Integration**: Secure Spotify API access
- **Environment Variables**: Sensitive data stored securely
- **CSRF Protection**: Built-in Flask-WTF protection

## Technologies Used

### Backend
- **Flask** - Web framework
- **SQLAlchemy** - Database ORM
- **Flask-Login** - User authentication
- **Spotipy** - Spotify API client
- **Groq** - AI API client

### Frontend
- **HTML5/CSS3** - Modern responsive design
- **JavaScript** - Interactive functionality
- **CSS Grid/Flexbox** - Layout system

### Database
- **PostgreSQL** - Production database
- **SQLite** - Development database

### AI & APIs
- **Groq AI** - Mood analysis
- **Spotify Web API** - Music integration

## Deployment

### Production Setup

1. **Set production environment variables**
2. **Use PostgreSQL database**
3. **Set strong SECRET_KEY**
4. **Configure reverse proxy (nginx)**
5. **Enable SSL/TLS**
6. **Set up monitoring**

### Docker Deployment (Optional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app.py"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **Groq** for providing powerful AI models
- **Spotify** for their excellent Web API
- **Flask** community for the amazing framework
- **VADER** (original sentiment analysis inspiration)

---

**Made with ❤️ and 🎵**

Transform your emotions into the perfect playlist with AI-powered mood analysis!