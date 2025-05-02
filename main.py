
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foundation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    amount = db.Column(db.Float)
    email = db.Column(db.String(120))

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    course = db.Column(db.String(100))

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    message = db.Column(db.Text)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return """
    <h1>Shashikala Foundation API</h1>
    <p>Available endpoints:</p>
    <ul>
        <li>POST /api/donate - Process donations</li>
        <li>POST /api/register - Handle registrations</li>
        <li>POST /api/contact - Submit contact form</li>
        <li>GET /api/donations - View donations</li>
        <li>GET /api/registrations - View registrations</li>
    </ul>
    """

@app.route('/api/donate', methods=['POST'])
def donate():
    data = request.json
    donation = Donation(name=data.get('name'), amount=data.get('amount'), email=data.get('email'))
    db.session.add(donation)
    db.session.commit()
    return jsonify({"message": "Donation recorded successfully"}), 201

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    registration = Registration(name=data.get('name'), email=data.get('email'), course=data.get('course'))
    db.session.add(registration)
    db.session.commit()
    return jsonify({"message": "Registration successful"}), 201

@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.json
    contact = Contact(name=data.get('name'), email=data.get('email'), message=data.get('message'))
    db.session.add(contact)
    db.session.commit()
    return jsonify({"message": "Message sent successfully"}), 201

@app.route('/api/donations', methods=['GET'])
def get_donations():
    donations = Donation.query.all()
    return jsonify([{
        'id': d.id,
        'name': d.name,
        'amount': d.amount,
        'email': d.email
    } for d in donations])

@app.route('/api/registrations', methods=['GET'])
def get_registrations():
    registrations = Registration.query.all()
    return jsonify([{
        'id': r.id,
        'name': r.name,
        'email': r.email,
        'course': r.course
    } for r in registrations])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
