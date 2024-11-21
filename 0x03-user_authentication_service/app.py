#!/usr/bin/env python3
""" flask app
"""
from flask import Flask, jsonify
from auth import Auth
from db import DB
import bcrypt


AUTH = Auth()

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/', methods=['GET'])
def Bienvenue() -> str:
    """ first route
    """
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=['POST'])
def users(request) -> "Response":
    """ users route
    """
    email = request.form.get('email')
    password = request.form.get('password')
    missing_field = "email" if not email else "password" if not password else None
    if missing_field:
        return jsonify({"message": f"{missing_field} is missing"}), 400

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "User created"}), 201
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")