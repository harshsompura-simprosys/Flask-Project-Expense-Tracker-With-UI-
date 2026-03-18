from flask import Blueprint, render_template, request, redirect, jsonify
from db import users_collection
from flask_jwt_extended import create_access_token, set_access_cookies,unset_jwt_cookies
from werkzeug.security import generate_password_hash ,check_password_hash



auth_bp = Blueprint("auth", __name__,template_folder="./templates")



@auth_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")


@auth_bp.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return "All fields required"
    hashed_password = generate_password_hash(password)
    users_collection.insert_one({
        "username": username,
        "password": hashed_password
    })

    return redirect("/login")

@auth_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.form

    
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password required"}), 400

    
    user = users_collection.find_one({
        "username": data["username"],
        "password": data["password"]
    })
    if user and check_password_hash(user["password"],data["password"]):
        token = create_access_token(identity=data["username"])
        response = redirect("/dashboard")

        set_access_cookies(response, token)

        return response
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@auth_bp.route("/logout")
def logout():
    response = redirect("/login")
    unset_jwt_cookies(response)
    return response