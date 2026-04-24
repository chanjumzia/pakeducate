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
    
    # New fields for detailed user information
    full_name = db.Column(db.String(120), nullable=True)
    father_name = db.Column(db.String(120), nullable=True)
    cnic = db.Column(db.String(15), nullable=True, unique=True)
    phone = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(120), nullable=True, unique=True)
    address = db.Column(db.String(250), nullable=True)
    marital_status = db.Column(db.String(20), nullable=True)

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
    if not user:
        session.clear() # Clear invalid session
        return redirect(url_for('login'))

    role = user.role
    username = user.username

    # Render the correct dashboard based on the user's role
    if role == 'Admin':
        return render_template('admin_dashboard.html', username=username)
    # ADDED: Principal role routing
    elif role == 'Principal':
        return render_template('admin_dashboard.html', username=username) # Can have a separate dashboard later
    elif role == 'Accountant':
        return render_template('accountant_dashboard.html', username=username)
    elif role == 'Teacher':
        return render_template('teacher_dashboard.html', username=username)
    else:
        # Fallback for unknown roles
        return redirect(url_for('logout'))

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
            # On successful login, always go to the welcome page first
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
    # Allow access if no users exist or if logged-in user is an Admin/Principal.
    allowed_roles = ['Admin', 'Principal']
    if User.query.count() > 0 and session.get('role') not in allowed_roles:
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        # New fields from the form
        full_name = request.form['full_name']
        father_name = request.form['father_name']
        cnic = request.form['cnic']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        marital_status = request.form['marital_status']

        # Check for existing username, email, or CNIC
        if User.query.filter_by(username=username).first():
            return render_template('register.html', message='یہ صارف نام پہلے سے موجود ہے')
        if User.query.filter(User.email.isnot(None)).filter_by(email=email).first():
            return render_template('register.html', message='یہ ای میل پہلے سے موجود ہے')
        if User.query.filter(User.cnic.isnot(None)).filter_by(cnic=cnic).first():
            return render_template('register.html', message='یہ شناختی کارڈ نمبر پہلے سے موجود ہے')

        new_user = User(
            username=username, 
            role=role,
            full_name=full_name,
            father_name=father_name,
            cnic=cnic,
            phone=phone,
            email=email,
            address=address,
            marital_status=marital_status
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        # If admin/principal created the user, go back to their dashboard.
        if session.get('role') in allowed_roles:
            # We will later add a success message here
            return redirect(url_for('index')) 
        else: # First user registration
            return redirect(url_for('login'))

    return render_template('register.html', message=None)

@app.route('/welcome')
def welcome():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('welcome.html', username=session.get('username'))

# The create_all call should be handled by a separate script now.
# We will not run it directly in app.py anymore for production safety.

if __name__ == '__main__':
    # Note: For development, you might still want db.create_all() here.
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True, port=5000)

