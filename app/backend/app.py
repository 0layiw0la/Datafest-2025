import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate  # Add this import
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from math import radians, cos, sin, asin, sqrt
import requests
import threading
import time


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)  # Add this line

# Enable CORS for the React frontend
CORS(app, supports_credentials=True, origins=["http://localhost:5173","https://cyberfarmdf.netlify.app"])


@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data['username']
        password = generate_password_hash(data['password'])
        phone = data['phone']
        role = data['role']
        latitude = data['latitude']
        longitude = data['longitude']

        new_user = User(username=username, password=password, phone=phone, role=role,
                        latitude=latitude, longitude=longitude)
        db.session.add(new_user)
        db.session.commit()
        print(f"[INFO] /api/register: Registration successful for user '{username}'")
        return jsonify({'message': 'Registration successful'})
    except Exception as e:
        print(f"[ERROR] /api/register: Registration failed - {e}")
        return jsonify({'message': 'Registration failed'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            print(f"[INFO] /api/login: Login successful for user '{username}'")
            return jsonify({'message': 'Login successful', 'user': {'username': user.username, 'role': user.role}})
        print(f"[WARNING] /api/login: Login failed for user '{username}'")
        return jsonify({'message': 'Invalid username or password'}), 401
    except Exception as e:
        print(f"[ERROR] /api/login: Login failed - {e}")
        return jsonify({'message': 'Login failed'}), 500

@app.route('/api/home', methods=['POST'])
def home():
    try:
        data = request.json
        username = data.get('username')  # Get the username from the request
        search_role = data.get('search_role')

        # Fetch the user from the database
        current_user = User.query.filter_by(username=username).first()
        if not current_user:
            print(f"[WARNING] /api/home: User '{username}' not found in the database")
            return jsonify({'message': 'Unauthorized'}), 401

        users = User.query.filter_by(role=search_role).all()
        current_location = (current_user.latitude, current_user.longitude)

        def haversine(lat1, lon1, lat2, lon2):
            lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a))
            r = 6371  # Radius of earth in kilometers
            return c * r

        # Calculate distances for users in the database
        user_distances = []
        for user in users:
            distance = haversine(current_user.latitude, current_user.longitude, user.latitude, user.longitude)
            user_distances.append((user, distance))
        user_distances.sort(key=lambda x: x[1])
        nearest_users = [{'username': u.username, 'latitude': u.latitude, 'longitude': u.longitude, 'phone': u.phone} for u, _ in user_distances[:10]]

        # If fewer than 10 matches, call Google Places API
        if len(nearest_users) < 10:
            remaining_count = 10 - len(nearest_users)
            import json
            # Text Search (New) API
            text_search_url = "https://places.googleapis.com/v1/places:searchText"
            headers = {
                "Content-Type": "application/json",
                "X-Goog-Api-Key": os.getenv("GOOGLE_API_KEY"),
                "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location"
            }

            payload = {
                "textQuery": search_role,
                "pageSize": remaining_count,
                "locationBias": {
                    "circle": {
                        "center": {
                            "latitude": current_location[0],
                            "longitude": current_location[1]
                        },
                        "radius": 30000.0  # meters
                    }
                }
            }

            response = requests.post(text_search_url, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                places = response.json().get("places", [])
                for place in places:
                    nearest_users.append({
                        "username": place.get("displayName", {}).get("text", "Unknown Place"),
                        "latitude": place["location"]["latitude"],
                        "longitude": place["location"]["longitude"],
                        "phone": "N/A",  # Not available in Text Search response
                        "address": place.get("formattedAddress", "N/A")
                    })
                return jsonify({'nearest_users': nearest_users})
            else:
                print(f"[ERROR] Google Places Text Search API call failed: {response.text}")

    except Exception as e:
        print(f"[ERROR] /api/home: Failed to fetch nearest users - {e}")
        return jsonify({'message': 'Failed to fetch nearest users'}), 500


##cron jobs
@app.route('/cron', methods=['GET'])
def cron():
    print("[INFO] Cron job triggered")

def keep_alive():
    while True:
        try:
            requests.get("https://cyberfarm.onrender.com/cron")
            print("Pinged the app to keep it alive!")
        except Exception as e:
            print(f"Error pinging: {e}")
        time.sleep(15) 

# Start keep_alive() in a separate thread
threading.Thread(target=keep_alive, daemon=True).start()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    print("[INFO] Flask app is running...")
    app.run(host='0.0.0', port=5000)