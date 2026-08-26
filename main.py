# rules of a ReST API
# 1. Data is transferred as key value-pairs called JSON.Sending from JS as JSON Object and from python as dictionary
# 2. You must define routes/URL 
# 3. You must define a HTTP method(GET,POST,PUT,DELETE,PATCH)
# 4. You must define a status code(200,201,404,401,500)
# 200 → success,201 → created,400 → bad request,401 → unauthorized,404 — Not Found,409 → conflict (email exists),500 → server error

from flask import Flask,request,jsonify
from sqlalchemy import create_engine,select
from sqlalchemy.orm import Session
from models import Base,Product,Sale,Sales_detail,Purchase

app = Flask(__name__)

# Create a connection to the database using sqlalchemy engine
engine = create_engine("sqlite:///./flask_duka_api.db", echo=True)

# Create tables into the database using sqlachemy
Base.metadata.create_all(engine)

# Create a session to do sql transactions
session = Session(engine)

@app.route("/")
def home():
    if request.method == "GET":
        data = {"Flask API":"Version 1"}
        return jsonify(data), 200
    else:
        error = {"Error":"Method not allowed"}
        return jsonify(error), 405

@app.route("/products")
def products():
    if request.method=="GET":
        # fetch data from the database
        query = select(Product)
        products = session.scalars(query)

        results = []
        for prod in products:
            p = {"id":prod.id,
                "product_name":prod.product_name,
                 "buying_price":prod.buying_price,
                 "selling_price":prod.selling_price}
            results.append(p)
        return jsonify(results), 200
    
    elif request.method=="POST":
        data = request.get_json()
        if data["product_name"] == "" or data["buying_price"] =="" or data["selling_price"] == "":
            error = {"Error":"Ensure all fields are set"}
            return jsonify(error), 403
        else:
            # store in the database
            pass
    else:
        error = {"Error":"Method not allowed"}
        return jsonify(error), 405

@app.route("/sales")
def sales():
    if request.method=="GET":
        query=select(Sale)
        sales=session.scalars(query)

        sales_list = []
        for sale in sales:
            s = {"id":sale.id,
                "user_id":sale.user_id,
                "sale_date":sale.sale_date}
            sales_list.append(s)
        return jsonify(sales_list), 200
    
    elif request.method=="POST":
        data = request.get_json()
        if data["user_id"] == "" or data["sale_date"] == "":
            error = {"Error":"Ensure all fields are set"}
            return jsonify(error), 403
        else:
            pass
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
            s = {"id":sal.id,
                "product_id":sal.product_id,
                "sale_id":sal.sale_id,
                "quantity":sal.quantity}
            sales_details.append(s)
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
        purchase=session.scalars(query)




app.run(debug=True)