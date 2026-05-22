from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
import bcrypt
import jwt
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

client = MongoClient(
    os.getenv("MONGO_URI"),
    tls=True,
    tlsAllowInvalidCertificates=True
)

db = client.companyDB
users = db.users

SECRET_KEY = os.getenv("SECRET_KEY")


# HOME PAGE
@app.route("/")
def home():
    return render_template("login.html")


# DASHBOARD PAGE
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# TEST REGISTER
@app.route("/test-register")
def test_register():

    existing_user = users.find_one({
        "email": "admin@test.com"
    })

    if existing_user:
        return "User already exists"

    hashed_password = bcrypt.hashpw(
        "123456".encode("utf-8"),
        bcrypt.gensalt()
    )

    users.insert_one({
        "email": "admin@test.com",
        "password": hashed_password
    })

    return "User registered successfully"


# TEST LOGIN
@app.route("/test-login")
def test_login():

    email = "admin@test.com"
    password = "123456"

    user = users.find_one({
        "email": email
    })

    if not user:
        return "User not found"

    if bcrypt.checkpw(
        password.encode("utf-8"),
        user["password"]
    ):

        token = jwt.encode({
            "email": email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }, SECRET_KEY, algorithm="HS256")

        return f"Login Success Token: {token}"

    return "Invalid password"


# REGISTER API
@app.route("/register", methods=["POST"])
def register():

    data = request.json

    email = data["email"]
    password = data["password"]

    existing_user = users.find_one({
        "email": email
    })

    if existing_user:
        return jsonify({
            "message": "User already exists"
        }), 400

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    users.insert_one({
        "email": email,
        "password": hashed_password
    })

    return jsonify({
        "message": "User registered successfully"
    })


# LOGIN API
@app.route("/login", methods=["POST"])
def login():

    data = request.json

    email = data["email"]
    password = data["password"]

    user = users.find_one({
        "email": email
    })

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    if bcrypt.checkpw(
        password.encode("utf-8"),
        user["password"]
    ):

        token = jwt.encode({
            "email": email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({
            "token": token,
            "message": "Login successful"
        })

    return jsonify({
        "message": "Invalid password"
    }), 401


if __name__ == "__main__":
    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)