from app import app, db

with app.app_context():
    print("Database tables banayi ja rahi hain...")
    db.create_all()
    print("Database tables kamyabi se ban gayi hain.")
