
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# In-memory storage (replace with database in production)
donations = []
registrations = []
contacts = []

@app.route('/api/donate', methods=['POST'])
def donate():
    data = request.json
    donations.append(data)
    return jsonify({"message": "Donation recorded successfully"}), 201

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    registrations.append(data)
    return jsonify({"message": "Registration successful"}), 201

@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.json
    contacts.append(data)
    return jsonify({"message": "Message sent successfully"}), 201

@app.route('/api/donations', methods=['GET'])
def get_donations():
    return jsonify(donations)

@app.route('/api/registrations', methods=['GET'])
def get_registrations():
    return jsonify(registrations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
