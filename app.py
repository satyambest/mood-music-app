from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from functools import wraps
from mood_agent import MoodKeywordAgent
from models import db, User
import urllib.parse

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

agent = MoodKeywordAgent()

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
        keywords = analysis["search_keywords"][:8]
        query = " ".join(keywords)

        # simple Spotify search link
        spotify_url = "https://open.spotify.com/search/" + urllib.parse.quote(query)

        return render_template(
            "index.html",
            essay=essay,
            analysis=analysis,
            query=query,
            spotify_url=spotify_url
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