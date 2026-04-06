from flask import Blueprint,render_template,redirect,url_for,request
from flask_jwt_extended import jwt_required,get_jwt_identity
from db import expense_collection,users_collection
import math
from bson import ObjectId

exp_bp = Blueprint("exp",__name__,template_folder="./templates")

@exp_bp.route("/dashboard")
@jwt_required()
def dashboard():
    user = get_jwt_identity()

    category = request.args.get("category")
    date = request.args.get("date")
    page = request.args.get("page", 1, type=int)


    per_page = 5
    skip = (page - 1) * per_page

    query = {"user": user}

    if category:
        query["category"] = category

    if date:
        query["date"] = date


    expenses_coll = list(expense_collection.find(query).skip(skip)
        .limit(per_page))
    total_count = expense_collection.count_documents(query)
    total_pages = math.ceil(total_count / per_page)


    total = sum(int(exp["amount"]) for exp in expenses_coll)

    total_len = len(expenses_coll)

    
    return render_template("dsb.html",exp = expenses_coll,user=user,total = total,length = total_len,page=page,
        total_pages=total_pages)

@exp_bp.route("/add-expense")
@jwt_required()
def add_expense_page():
    return render_template("expenses.html")


@exp_bp.route("/add-expense",methods=["GET","POST"])
@jwt_required()
def add_expense():
    if request.method == "POST" : 
        user  = get_jwt_identity()
        data = request.form
        expense_collection.insert_one(
            {
                "title":data["title"],
                "amount" : data["amount"],
                "date" : data["date"] , 
                "category" : data["category"],
                "user" : user
            }
        )
    return redirect(url_for("exp.dashboard"))



@exp_bp.route("/update-expense/<string:id>",methods =["GET"])
@jwt_required()
def update_expense_page(id):
    expense = expense_collection.find_one({"_id":ObjectId(id)})
    return render_template("update_exp.html",expense = expense)

@exp_bp.route("/update-expense/<string:id>",methods=["POST"])
@jwt_required()
def update_expense(id):
    data = request.form
    updated_exp = expense_collection.update_one({"_id":ObjectId(id)},
        {
            "$set":{   
                "title":data["title"],
                "amount" : data["amount"],
                "date" : data["date"] , 
                "category" : data["category"]
            }
            }
    )
    if updated_exp.modified_count >0 :
        return redirect("/dashboard")
    return "error while updating"

@exp_bp.route("/delete/<string:id>",methods=["GET"])
def delete(id):
    exp =  expense_collection.delete_one({"_id":ObjectId(id)})
    if not exp:
        return "Deletion Failed"
    return redirect("/dashboard")

