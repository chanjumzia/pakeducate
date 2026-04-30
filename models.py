from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    father_name = db.Column(db.String(120), nullable=False)
    cnic = db.Column(db.String(15), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    address = db.Column(db.String(255), nullable=False)
    marital_status = db.Column(db.String(20), nullable=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    father_name = db.Column(db.String(120), nullable=False)
    class_name = db.Column(db.String(80), nullable=False)

class Fee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    student = db.relationship('Student', backref=db.backref('fees', lazy=True))
    month = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Unpaid')
