# rules of a ReST API
# 1. Data is transferred as key value-pairs called JSON.Sending from JS as JSON Object and from python as dictionary
# 2. You must define routes/URL 
# 3. You must define a HTTP method(GET,POST,PUT,DELETE,PATCH)
# 4. You must define a status code(200,201,404,401,500)
# 200 → success,201 → created,400 → bad request,401 → unauthorized,404 — Not Found,409 → conflict (email exists),500 → server error

from flask import Flask,request,jsonify
from sqlalchemy import create_engine,select
from sqlalchemy.orm import Session
from models import Base,Product,Sale,Sales_detail,Purchase,Payment,User

app = Flask(__name__)

# Create a connection to the database using sqlalchemy engine
engine = create_engine("sqlite:///./flask_duka_api.db", echo=True)

# Create tables into the database using sqlachemy
Base.metadata.create_all(engine)

# Create a session to do sql transactions
session = Session(engine)

user = {"id":"1",
        "full_name":"Binti",
        "email":"binti@gmail.com",
        "password":"binti5",
        "phone_number":"0717238745"}

@app.before_request
def before_request():
    try:
        print("A request is coming in!")
        new_user = User(user)
        session.add(new_user)
        session.commit()

        return jsonify({"Message":"User added successfully"}), 201
    except:
        print("Error found")

@app.route("/")
def home():
    if request.method == "GET":
        data = {"Flask API":"Version 1"}
        return jsonify(data), 200
    else:
        error = {"Error":"Method not allowed"}
        return jsonify(error), 405

@app.route("/products",methods = ["GET","POST"])
def products():
    if request.method=="GET":
        # fetch data from the database
        query = select(Product)
        products = session.scalars(query)

        results = []
        for prod in products:
            product = {"id":prod.id,
                "product_name":prod.product_name,
                 "buying_price":prod.buying_price,
                 "selling_price":prod.selling_price}
            results.append(product)
        return jsonify(results), 200
    
    elif request.method=="POST":
        data = request.get_json()
        if data["product_name"] == "" or data["buying_price"] =="" or data["selling_price"] == "":
            error = {"Error":"Ensure all fields are set"}
            return jsonify(error), 403
        else:
            # store in the database
            new_product = Product(
                user_id = user["id"],
                product_name = data["product_name"],
                buying_price = float(data["buying_price"]),
                selling_price = float(data["selling_price"])
            )
            session.add(new_product)
            session.commit()
            return jsonify({"Message":"A new product has been added successfully"}), 201
    else:
        error = {"Error":"Method not allowed"}
        return jsonify(error), 405

@app.route("/sales",methods = ["GET","POST"])
def sales():
    if request.method=="GET":
        query=select(Sale)
        sales=session.scalars(query)

        sales_list = []
        for sale in sales:
            sal = {"id":sale.id,
                "user_id":sale.user_id,
                "sale_date":sale.sale_date}
            sales_list.append(sal)
        return jsonify(sales_list), 200
    
    elif request.method=="POST":
        data = request.get_json()
        if data["sale_date"] == "":
            error = {"Error":"Ensure all fields are set"}
            return jsonify(error), 403
        else:
            new_sale = Sale(
                user_id = user["id"],
                sale_date = data["sale_date"]
            )
            session.add(new_sale)
            session.commit()
            return jsonify({"Message":"A new sale successfully added"}), 201
    else:
        error = {"Error":"Method not allowed"}
        return jsonify(error), 405

@app.route("/sales_details")
def sales_details():
    if request.method=="GET":
        query=select(Sales_detail)
        sales_details=session.scalars(query)

        sales_details = []
        for sal in sales_details:
            sal_d = {"id":sal.id,
                "product_id":sal.product_id,
                "sale_id":sal.sale_id,
                "quantity":sal.quantity}
            sales_details.append(sal_d)
        return jsonify(sales_details), 200
    
    elif request.method=="POST":
        data = request.get_json()
        if data["product_id"] == "" or data["sale_id"] == "" or data["quantity"]:
            error = {"Error":"Ensure all fields are set"}
            return jsonify(error), 403
        else:
            pass
    else:
        error = {"Error":"Method not allowed"}
        return jsonify(error), 405

@app.route("/purchases")
def purchases():
    if request.method=="GET":
        query=select(Purchase)
        purchases=session.scalars(query)

        purchase_list = []
        for purch in purchases:
            purchase = {"id":purch.id,
                 "product_id":purch.product_id,
                 "quantity":purch.quantity,
                 "buying_price":purch.quantity}
            purchase_list.append(purchase)
        return jsonify(purchase_list), 200

    elif request.method=="POST":
        data = request.get_json()
        if data["product_id"] == "" or data["quantity"] == "" or data["buying_price"]:
                error = {"Error":"Ensure all fields are set"}
                return jsonify(error), 403
        else:
            pass
    else:
        error = {"Error":"Method not allowed"}
        return jsonify(error), 405

@app.route("/payments")
def payments():
    if request.method=="GET":
        query=select(Payment)
        payments=session.scalars(query)

        payment_list = []
        for pay in payments:
            payment = {"id":pay.id,
                 "product_id":pay.product_id,
                 "quantity":pay.quantity,
                 "buying_price":pay.quantity}
            payment_list.append(payment)
        return jsonify(payment_list), 200

    elif request.method=="POST":
        data = request.get_json()
        if data["sales_id"] == "" or data["amount"] == "" or data["payment_method"] or data["payment_status"]:
                error = {"Error":"Ensure all fields are set"}
                return jsonify(error), 403
        else:
            pass
    else:
        error = {"Error":"Method not allowed"}
        return jsonify(error), 405

@app.route("/users")
def users():
    if request.method=="GET":
        query=select(User)
        users=session.scalars(query)

        user_list = []
        for use in users:
            user = {"id":use.id,
                 "full_name":use.full_name,
                 "email":use.email,
                 "password":use.password,
                 "phone_number":use.phone_number}
            user_list.append(user)
        return jsonify(user_list), 200

    elif request.method=="POST":
        data = request.get_json()
        if data["full_name"] == "" or data["email"] == "" or data["password"] or data["phone_number"]:
                error = {"Error":"Ensure all fields are set"}
                return jsonify(error), 403
        else:
            pass
    else:
        error = {"Error":"Method not allowed"}
        return jsonify(error), 405

app.run(debug=True)