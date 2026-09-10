# rules of a ReST API
# 1. Data is transferred as key value-pairs called JSON.Sending from JS as JSON Object and from python as dictionary
# 2. You must define routes/URL 
# 3. You must define a HTTP method(GET,POST,PUT,DELETE,PATCH)
# 4. You must define a status code(200,201,404,401,500)
# 200 → success,201 → created,400 → bad request,401 → unauthorized,404 — Not Found,409 → conflict (email exists),500 → server error

from dotenv import load_dotenv
import os
import sentry_sdk
from flask import Flask,request,jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager,jwt_required,create_access_token,get_jwt_identity
from sqlalchemy import create_engine,select
from sqlalchemy.orm import Session
from models import Base,Product,Sale,Sales_detail,Purchase,Payment,User
load_dotenv()

sentry_sdk.init(
    dsn="https://75ec0a83c7d77ca7a5e97099c3f25279@o4512046182760448.ingest.us.sentry.io/4512051094814720",
    send_default_pii=True,
)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt =  JWTManager(app)
bcrypt = Bcrypt(app)

# Create a connection to the database using sqlalchemy engine
engine = create_engine("sqlite:///./flask_duka_api.db", echo=True)

# Create tables into the database using sqlachemy
Base.metadata.create_all(engine)

# Create a session to do sql transactions
session = Session(engine)

allowed_methods = ["GET","POST","DELETE","PATCH","PUT"]

@app.before_request
def before_request():
    try:
        pass
    except:
        pass

@app.route("/",methods = allowed_methods)
def home():
    if request.method == "GET":
        data = {"Flask API" : "Version 1"}
        return jsonify(data), 200
    else:
        error = {"Error":"Method not allowed"}
        return jsonify(error), 405

@app.route("/register",methods = allowed_methods)
def register():
    if request.method=="POST":
        try:
            data = request.get_json()

            if not data.get("full_name") or not data.get("email") or not data.get("password") or not data.get("phone_number"):
                error = {"Error":"Ensure all fields are set"}
                return jsonify(error), 403

            existing_user = session.query(User).filter_by(email=data["email"]).first()

            if existing_user:
                error = {"Error":"Email already registered"}
                return jsonify(error), 409

            hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')

            new_user = User(
                full_name=data["full_name"],
                email=data["email"],
                password=hashed_pw,
                phone_number=data["phone_number"]
            )

            session.add(new_user)
            session.commit()

            token = create_access_token(identity=data["email"])

            message = {"Message":"User registered successfully",
                    "token":token}
            return jsonify(message), 201
        
        except Exception as e:
            sentry_sdk.capture_exception(e)
            return jsonify({"error": "Something went wrong"}), 500
        
    else:
        error = {"Error":"Method not allowed"}
        return jsonify(error), 405

@app.route("/login", methods = allowed_methods)
def login():
    if request.method == "POST":
        try:
            data = request.get_json()

            if not data.get("email") or not data.get("password"):
                error = {"Error":"Ensure all fields are set"}
                return jsonify(error), 403
            
            email=data["email"]
            password=data["password"]
            
            query = select(User).where(User.email==email)  
            existing_user = session.scalars(query).first()

            if not existing_user:
                error = {"Error":"Invalid email"}
                return jsonify(error), 403
                
            if not bcrypt.check_password_hash(existing_user.password, password):
                error = {"Error":"Invalid password"}
                return jsonify(error), 403

            token = create_access_token(identity=email)

            return jsonify({
                    "message":"Login successful",
                    "user": {
                        "id": existing_user.id,
                        "email":existing_user.email,
                        "full_name":existing_user.full_name
                        },
                    "token":token
                }), 200
        
        except Exception as e:
                sentry_sdk.capture_exception(e)
                return jsonify({"error": "Something went wrong"}), 500
    
    else:
        error = {"Error":"Method not allowed"}
        return jsonify(error), 405

@app.route("/products",methods = allowed_methods)
@jwt_required()
def products():
    try:
        email = get_jwt_identity()

        user = session.scalars(select(User).where(User.email==email)).first()

        if request.method=="GET":
            # fetch data from the database
            query = select(Product)
            products = session.scalars(query)

            products_list = []
            for prod in products:
                product = {
                    "id":prod.id,
                    "product_name":prod.product_name,
                    "buying_price":prod.buying_price,
                    "selling_price":prod.selling_price
                    }
                products_list.append(product)
            return jsonify(products_list), 200
        
        elif request.method=="POST":
            data = request.get_json()
            if not data.get("product_name") or not data.get("buying_price") or not data.get("selling_price"):
                error = {"Error":"Ensure all fields are set"}
                return jsonify(error), 403
            else:
                # store in the database
                new_product = Product(
                    user_id = user.id,
                    product_name = data["product_name"],
                    buying_price = float(data["buying_price"]),
                    selling_price = float(data["selling_price"])
                )
                session.add(new_product)
                session.commit()

                message = {"Message":"Product added successfully"}
                return jsonify(message), 201
        else:
            error = {"Error":"Method not allowed"}
            return jsonify(error), 405
        
    except Exception as e:
            sentry_sdk.capture_exception(e)
            return jsonify({"error": "Something went wrong"}), 500

@app.route("/sales",methods = allowed_methods)
@jwt_required()
def sales():
    try:
        email = get_jwt_identity()
        
        user = session.scalars(select(User).where(User.email==email)).first()
        if request.method=="GET":
            query=select(Sale)
            sales=session.scalars(query)

            sales_list = []
            for sale in sales:
                sal = {
                    "id":sale.id,
                    "user_id":sale.user_id,
                    "sale_date":sale.sale_date
                    }
                sales_list.append(sal)
            return jsonify(sales_list), 200
        
        elif request.method=="POST":
            data = request.get_json()
            
            new_sale = Sale(
                    user_id = user.id
                )
            session.add(new_sale)
            session.commit()

            message = {"Message":"Sales added successfully"}
            return jsonify(message), 201
        
        else:
            error = {"Error":"Method not allowed"}
            return jsonify(error), 405
        
    except Exception as e:
            sentry_sdk.capture_exception(e)
            return jsonify({"error": "Something went wrong"}), 500
    
@app.route("/sales-details",methods = allowed_methods)
@jwt_required()
def sales_details():
    try:
        email = get_jwt_identity()
        
        user = session.scalars(select(User).where(User.email==email)).first()
        if request.method=="GET":
            query=select(Sales_detail)
            sales_details=session.scalars(query)

            sales_details_list = []
            for sal in sales_details:
                sal_d = {
                    "id":sal.id,
                    "product_id":sal.product_id,
                    "sales_id":sal.sales_id,
                    "quantity":sal.quantity
                    }
                sales_details_list.append(sal_d)
            return jsonify(sales_details_list), 200
        
        elif request.method=="POST":
            data = request.get_json()
            if not data.get("product_id") or not data.get("sales_id") or not data.get("quantity"):
                error = {"Error":"Ensure all fields are set"}
                return jsonify(error), 403
            else:
                new_sale_details = Sales_detail(
                    product_id = data["product_id"],
                    sales_id = data["sales_id"],
                    quantity = data["quantity"]
                )
                session.add(new_sale_details)
                session.commit()
                message = {"Message":"Sales_details added successfully"}
                return jsonify(message), 201
        else:
            error = {"Error":"Method not allowed"}
            return jsonify(error), 405
        
    except Exception as e:
                sentry_sdk.capture_exception(e)
                return jsonify({"error": "Something went wrong"}), 500
    
@app.route("/purchases",methods = allowed_methods)
@jwt_required()
def purchases():
    try:
        email = get_jwt_identity()
        
        user = session.scalars(select(User).where(User.email==email)).first()
        if request.method=="GET":
            query=select(Purchase)
            purchases=session.scalars(query)

            purchase_list = []
            for purch in purchases:
                purchase = {
                    "id":purch.id,
                    "product_id":purch.product_id,
                    "quantity":purch.quantity,
                    "buying_price":purch.buying_price
                    }
                purchase_list.append(purchase)
            return jsonify(purchase_list), 200

        elif request.method=="POST":
            data = request.get_json()
            if not data.get("product_id") or not data.get("quantity") or not data.get("buying_price"):
                    error = {"Error":"Ensure all fields are set"}
                    return jsonify(error), 403
            else:
                new_purchase = Purchase(
                    product_id = data["product_id"],
                    quantity = data["quantity"],
                    buying_price = float(data["buying_price"])
                )
                session.add(new_purchase)
                session.commit()

                message = {"Message":"Purchases added successfully"}
                return jsonify(message), 201
        else:
            error = {"Error":"Method not allowed"}
            return jsonify(error), 405
        
    except Exception as e:
            sentry_sdk.capture_exception(e)
            return jsonify({"error": "Something went wrong"}), 500
    
@app.route("/payments",methods = allowed_methods)
@jwt_required()
def payments():
    try:
        email = get_jwt_identity()
        
        user = session.scalars(select(User).where(User.email==email)).first()
        if request.method=="GET":
            query=select(Payment)
            payments=session.scalars(query)

            payment_list = []
            for pay in payments:
                payment = {
                    "id":pay.id,
                    "sales_id":pay.sales_id,
                    "amount":pay.amount,
                    "payment_method":pay.payment_method,
                    "payment_status":pay.payment_status
                    }
                payment_list.append(payment)
            return jsonify(payment_list), 200

        elif request.method=="POST":
            data = request.get_json()
            if not data.get("sales_id") or not data.get("amount") or not data.get("payment_method") or not data.get("payment_status"):
                    error = {"Error":"Ensure all fields are set"}
                    return jsonify(error), 403
            else:
                new_payment = Payment(
                    sales_id = data["sales_id"],
                    amount = float(data["amount"]),
                    payment_method = data["payment_method"],
                    payment_status = data["payment_status"]
                )
                session.add(new_payment)
                session.commit()

                message = {"Message":"Payments added successfully"}
                return jsonify(message), 201
        else:
            error = {"Error":"Method not allowed"}
            return jsonify(error), 405
        
    except Exception as e:
            sentry_sdk.capture_exception(e)
            return jsonify({"error": "Something went wrong"}), 500
    
@app.route("/users",methods = allowed_methods)
def users():
    try:
        if request.method=="GET":
            query=select(User)
            users=session.scalars(query)

            user_list = []
            for use in users:
                user = {
                    "id":use.id,
                    "full_name":use.full_name,
                    "email":use.email,
                    "phone_number":use.phone_number
                    }
                user_list.append(user)
            return jsonify(user_list), 200

        elif request.method=="POST":
            data = request.get_json()
            if not data.get("full_name") or not data.get("email") or not data.get("password") or not data.get("phone_number"):
                    error = {"Error":"Ensure all fields are set"}
                    return jsonify(error), 403
            else:
                hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')

                new_user = User(
                    full_name = data["full_name"],
                    email = data["email"],
                    password = hashed_pw,
                    phone_number = data["phone_number"]
                )
                session.add(new_user)
                session.commit()

                message = {"Message":"User added successfully"}
                return jsonify(message), 201
        else:
            error = {"Error":"Method not allowed"}
            return jsonify(error), 405
        
    except Exception as e:
            sentry_sdk.capture_exception(e)
            return jsonify({"error": "Something went wrong"}), 500


app.run(debug=True)