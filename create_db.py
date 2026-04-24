from app import app, db

with app.app_context():
    # This creates all the tables based on your models in app.py
    db.create_all()

print("Database tables created successfully.")
