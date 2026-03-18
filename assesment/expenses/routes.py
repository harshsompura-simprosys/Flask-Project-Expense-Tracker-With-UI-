from flask import Blueprint,render_template,redirect,url_for,request
from flask_jwt_extended import jwt_required,get_jwt_identity
from db import expense_collection

exp_bp = Blueprint("exp",__name__,template_folder="./templates")

# @exp_bp.routes("/dashboard")
# @jwt_required()
# def dashboard():
#     user = get_jwt_identity()
#     return f'Welcome {user} '

# @exp_bp.routes("/add-task",methods = ["POST"])
# @jwt_required
# def add_task():
#     data = request.form
