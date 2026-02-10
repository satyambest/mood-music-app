from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from functools import wraps
from mood_agent import MoodKeywordAgent
from models import db, User
import urllib.parse
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables from .env file
load_dotenv()

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')  # Change this in production

# PostgreSQL configuration
database_url = os.environ.get('DATABASE_URL')
if database_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Fallback to SQLite for development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

agent = MoodKeywordAgent()

# Spotify OAuth setup
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=url_for('spotify_callback', _external=True),
        scope='playlist-modify-public playlist-modify-private user-read-private user-read-email'
    )

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Admin access required")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        essay = request.form.get("essay", "")

        if not essay.strip():
            return render_template("index.html", error="Please write something 😊")

        analysis = agent.generate_keywords(essay)
        
        # Use spotify_search_keywords if available, otherwise fall back to search_keywords
        spotify_keywords = analysis.get("spotify_search_keywords", [])
        if not spotify_keywords:
            spotify_keywords = analysis["search_keywords"][:8]
        
        query = " ".join(spotify_keywords[:8])

        # Get Spotify search results if user is connected
        spotify_tracks = []
        if current_user.spotify_token:
            try:
                sp = spotipy.Spotify(auth=current_user.spotify_token)
                results = sp.search(q=query, type='track', limit=5)
                for track in results['tracks']['items']:
                    spotify_tracks.append({
                        'id': track['id'],
                        'name': track['name'],
                        'artist': track['artists'][0]['name'],
                        'album': track['album']['name'],
                        'image': track['album']['images'][0]['url'] if track['album']['images'] else None,
                        'uri': track['uri'],
                        'external_url': track['external_urls']['spotify']
                    })
            except Exception as e:
                print(f"Spotify search error: {e}")

        # simple Spotify search link
        spotify_url = "https://open.spotify.com/search/" + urllib.parse.quote(query)

        return render_template(
            "index.html",
            essay=essay,
            analysis=analysis,
            query=query,
            spotify_url=spotify_url,
            spotify_tracks=spotify_tracks,
            spotify_connected=bool(current_user.spotify_token)
        )

    # first time: just show empty page
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password")

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if User.query.filter_by(username=username).first():
            flash("Username already exists")
        elif User.query.filter_by(email=email).first():
            flash("Email already exists")
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("index"))

    return render_template("signup.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/admin")
@login_required
@admin_required
def admin():
    users = User.query.all()
    return render_template("admin.html", users=users)


@app.route("/admin/user/<int:user_id>/toggle_admin", methods=["POST"])
@login_required
@admin_required
def toggle_admin(user_id):
    user = db.session.get(User, user_id)
    if user.id == current_user.id:
        flash("Cannot modify your own admin status")
        return redirect(url_for("admin"))

    user.is_admin = not user.is_admin
    db.session.commit()
    flash(f"Admin status updated for {user.username}")
    return redirect(url_for("admin"))


@app.route("/admin/user/<int:user_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if user.id == current_user.id:
        flash("Cannot delete your own account")
        return redirect(url_for("admin"))

    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.username} deleted")
    return redirect(url_for("admin"))


@app.route('/spotify/login')
@login_required
def spotify_login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/spotify/callback')
@login_required
def spotify_callback():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    
    # Store Spotify token in user's session/database
    current_user.spotify_token = token_info['access_token']
    current_user.spotify_refresh_token = token_info.get('refresh_token')
    db.session.commit()
    
    return redirect(url_for('index'))


@app.route('/spotify/search')
@login_required
def spotify_search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'No search query provided'}), 400
    
    # Get user's Spotify token
    token = current_user.spotify_token
    if not token:
        return jsonify({'error': 'Spotify not connected'}), 401
    
    try:
        sp = spotipy.Spotify(auth=token)
        results = sp.search(q=query, type='track', limit=10)
        
        tracks = []
        for track in results['tracks']['items']:
            tracks.append({
                'id': track['id'],
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'image': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'preview_url': track['preview_url'],
                'external_url': track['external_urls']['spotify']
            })
        
        return jsonify({'tracks': tracks})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/spotify/create_playlist', methods=['POST'])
@login_required
def create_playlist():
    playlist_name = request.form.get('name', 'Mood DJ Playlist')
    description = request.form.get('description', 'Created by Mood DJ')
    
    token = current_user.spotify_token
    if not token:
        return jsonify({'error': 'Spotify not connected'}), 401
    
    try:
        sp = spotipy.Spotify(auth=token)
        user_id = sp.current_user()['id']
        
        playlist = sp.user_playlist_create(
            user=user_id,
            name=playlist_name,
            public=True,
            description=description
        )
        
        return jsonify({
            'success': True,
            'playlist_id': playlist['id'],
            'playlist_url': playlist['external_urls']['spotify']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/spotify/add_to_playlist', methods=['POST'])
@login_required
def add_to_playlist():
    playlist_id = request.form.get('playlist_id')
    track_uri = request.form.get('track_uri')
    
    if not playlist_id or not track_uri:
        return jsonify({'error': 'Missing playlist_id or track_uri'}), 400
    
    token = current_user.spotify_token
    if not token:
        return jsonify({'error': 'Spotify not connected'}), 401
    
    try:
        sp = spotipy.Spotify(auth=token)
        sp.playlist_add_items(playlist_id, [track_uri])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/spotify/playlists')
@login_required
def get_playlists():
    token = current_user.spotify_token
    if not token:
        return jsonify({'error': 'Spotify not connected'}), 401
    
    try:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.current_user_playlists(limit=20)
        
        playlist_list = []
        for playlist in playlists['items']:
            playlist_list.append({
                'id': playlist['id'],
                'name': playlist['name'],
                'tracks': playlist['tracks']['total'],
                'url': playlist['external_urls']['spotify']
            })
        
        return jsonify({'playlists': playlist_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # Create admin user if it doesn't exist
        if not User.query.filter_by(username="admin").first():
            admin_user = User(username="admin", email="admin@example.com", is_admin=True)
            admin_user.set_password("admin123")
            db.session.add(admin_user)
            db.session.commit()
    app.run(debug=True) 