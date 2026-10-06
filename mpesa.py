from dotenv import load_dotenv
import os
load_dotenv()
import time
import math
import base64
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
saf_api_url = os.getenv("SAF_API_URL")
saf_short_code = os.getenv("SAF_SHORT_CODE")
saf_passkey = os.getenv("SAF_PASSKEY")
saf_stk_push =  os.getenv("SAF_STK_PUSHURL")
my_callback_url = os.getenv("MY_CALLback_URL")

def generate_password_and_timestamp():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password_str = saf_short_code + saf_passkey + timestamp
    password_bytes = password_str.encode()
    password = base64.b64encode(password_bytes).decode("utf-8")
    return password, timestamp

def get_mpesa_access_token():
    try:
        res = requests.get(
            saf_api_url,
            auth=HTTPBasicAuth(consumer_key, consumer_secret),
        )
        return res.json()['access_token']
    except Exception as e:
        print(str(e), "error getting access token")
        raise e

def make_stk_push(payload):
    amount = payload['amount']
    phone_number = payload['phone_number']
    sale_id = payload.get('sale_id')  

    # Dynamically generate token and password on every push
    token = get_mpesa_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    password, timestamp = generate_password_and_timestamp()

    push_data = {
        "BusinessShortCode": saf_short_code,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": math.ceil(float(amount)),
        "PartyA": phone_number,
        "PartyB": saf_short_code,
        "PhoneNumber": phone_number,
        "CallBackURL": my_callback_url,
        "AccountReference": str(payload.get('sale_id')),
        "TransactionDesc": "description of the transaction",
    }

    response = requests.post(
        saf_stk_push,
        json=push_data,
        headers=headers)

    return response.json()
