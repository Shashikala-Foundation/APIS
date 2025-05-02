
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shashikala.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class EventRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100), nullable=False)
    participant_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='registered')
    
class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    email = db.Column(db.String(120))
    message = db.Column(db.Text)

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    email = db.Column(db.String(120), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    primary_address = db.Column(db.String(200), nullable=False)
    apt_unit_suite = db.Column(db.String(50))
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.String(10), nullable=False)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/api/donate', methods=['POST'])
def donate():
    data = request.json
    try:
        donation = Donation(
            name=data['name'],
            amount=data['amount'],
            email=data.get('email'),
            message=data.get('message')
        )
        db.session.add(donation)
        db.session.commit()
        return jsonify({"message": "Donation recorded successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    required_fields = ['first_name', 'last_name', 'email', 'contact', 
                      'primary_address', 'city', 'state', 'zipcode']
    
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    try:
        registration = Registration(**data)
        db.session.add(registration)
        db.session.commit()
        return jsonify({"message": "Registration successful"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.json
    try:
        contact = Contact(
            name=data['name'],
            email=data['email'],
            message=data['message']
        )
        db.session.add(contact)
        db.session.commit()
        return jsonify({"message": "Message sent successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/api/donations', methods=['GET'])
def get_donations():
    donations = Donation.query.all()
    return jsonify([{
        'id': d.id,
        'name': d.name,
        'amount': d.amount,
        'email': d.email,
        'message': d.message
    } for d in donations])

@app.route('/api/registrations', methods=['GET'])
def get_registrations():
    registrations = Registration.query.all()
    return jsonify([{
        'id': r.id,
        'first_name': r.first_name,
        'last_name': r.last_name,
        'email': r.email,
        'contact': r.contact
    } for r in registrations])

@app.route('/api/events/register', methods=['POST'])
def register_event():
    data = request.json
    try:
        event_registration = EventRegistration(
            event_name=data['event_name'],
            participant_name=data['participant_name'],
            email=data['email'],
            phone=data['phone'],
            registration_date=datetime.now(),
            status=data.get('status', 'registered')
        )
        db.session.add(event_registration)
        db.session.commit()
        return jsonify({"message": "Event registration successful"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/api/events/registrations', methods=['GET'])
def get_event_registrations():
    event_registrations = EventRegistration.query.all()
    return jsonify([{
        'id': r.id,
        'event_name': r.event_name,
        'participant_name': r.participant_name,
        'email': r.email,
        'phone': r.phone,
        'registration_date': r.registration_date.isoformat(),
        'status': r.status
    } for r in event_registrations])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
