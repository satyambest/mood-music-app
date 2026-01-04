#!/usr/bin/env python3
"""
Database initialization script for Mood DJ app.
This script creates the database tables and sets up the default admin user.
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User

def init_database():
    """Initialize the database with tables and default data."""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()

        # Create default admin user if it doesn't exist
        if not User.query.filter_by(username="admin").first():
            print("Creating default admin user...")
            admin_user = User(
                username="admin",
                email="admin@example.com",
                is_admin=True
            )
            admin_user.set_password("admin123")
            db.session.add(admin_user)
            db.session.commit()
            print("✓ Default admin user created (username: admin, password: admin123)")
        else:
            print("✓ Admin user already exists")

        print("✓ Database initialization complete!")

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    print("Initializing Mood DJ database...")
    print(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI'][:50]}...")

    try:
        init_database()
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)