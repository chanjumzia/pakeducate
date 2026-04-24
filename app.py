from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

# App Initialization
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'pakeducate.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Database Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    def set_password(self, password): self.password_hash = generate_password_hash(password)
    def check_password(self, password): return check_password_hash(self.password_hash, password)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    father_name = db.Column(db.String(120), nullable=False)

# --- Routing Logic ---

@app.route('/landing')
def landing():
    return render_template('landing.html')

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('index.html', user_role=user.role if user else 'N/A')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['role'] = user.role
            session['username'] = user.username
            return redirect(url_for('welcome'))
        else:
            show_register_link = User.query.count() == 0
            return render_template('login.html', error='غلط صارف نام یا پاس ورڈ', show_register_link=show_register_link)
    
    show_register_link = User.query.count() == 0
    return render_template('login.html', show_register_link=show_register_link)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Authorization check: 
    # Allow access if no users exist (for the first user)
    # Or if the logged-in user is an Admin.
    if User.query.count() > 0 and session.get('role') != 'Admin':
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        if User.query.filter_by(username=username).first():
            return render_template('register.html', message='یہ صارف نام پہلے سے موجود ہے')

        new_user = User(username=username, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        # If an admin created the user, go back to index, otherwise to login.
        if session.get('role') == 'Admin':
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))

    # For a GET request, just show the registration page.
    # Pass message as None to avoid template errors if it's not set.
    return render_template('register.html', message=None)

@app.route('/welcome')
def welcome():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('welcome.html', username=session.get('username'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)