from dotenv import load_dotenv
import os
load_dotenv()
import time,math,base64,requests
from datetime import datetime
from requests.auth import HTTPBasicAuth

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
saf_api_url = os.getenv("SAF_API_URL")
saf_short_code = os.getenv("SAF_SHORT_CODE")
saf_passkey = os.getenv("SAF_PASSKEY")
saf_stk_pushurl =  os.getenv("SAF_STK_PUSHURL")
my_callback_url = os.getenv("MY_CALLback_URL")

def generate_password_and_timestamp():
    # This gets the current date and time since M-Pesa requires this timestamp when making an STK Push.
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    # This creates the string used to generate the STK Push password.
    password_str = saf_short_code + saf_passkey + timestamp
    # This converts the normal Python string into bytes.Because Base64 encoding works with bytes.
    password_bytes = password_str.encode()
    # This Base64 encodes the string to something like MTc0Mzc5YW... since M-Pesa expects the password in Base64 format.
    password = base64.b64encode(password_bytes).decode("utf-8")
    return password, timestamp

#creating a function whose job is to get an access token from Safaricom.
def get_mpesa_access_token():
    try:
        #An application sends a request to Safaricom providing consumer_key and consumer_secret
        res = requests.get(
            saf_api_url,
            auth=HTTPBasicAuth(consumer_key, consumer_secret),
        )
        # Safaricom responds with JSON containing an access token which is valid for an hour.
        return res.json()['access_token']
    except Exception as e:
        print(str(e), "error getting access token")
        raise e

# This function receives payment information stored in payload.
def make_stk_push(payload):
    # Getting amount,phone number and the sale ID
    amount = payload['amount']
    phone_number = payload['phone_number']
    # The .get() is useful because if sale_id doesn't exist, Python returns none not a keyerror
    sale_id = payload.get('sale_id')  

    # Dynamically generate token and password on every push
    token = get_mpesa_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # getting the password and timestamp
    password, timestamp = generate_password_and_timestamp()

    # api gives safaricom everything it needs to create this payment request.
    push_data = {
        "BusinessShortCode": saf_short_code,
        "Password": password,
        "Timestamp": timestamp,
        # This tells M-Pesa what type of transaction you're requesting.In this case:Customer is paying your PayBill online.
        "TransactionType": "CustomerPayBillOnline",
        "Amount": math.ceil(float(amount)),
        # This is the customer's phone number or the person paying.
        "PartyA": phone_number,
        "PartyB": saf_short_code,
        # This is the customer's phone number or the person paying.
        "PhoneNumber": phone_number,
        # After the customer responds to the STK prompt, Safaricom needs to tell your Flask application what happened.
        # CallBackURL is the address Safaricom uses to report the result of the payment.
        "CallBackURL": my_callback_url,
        # This connects the M-Pesa payment to your sale.
        "AccountReference": str(payload.get('sale_id')),
        "TransactionDesc": "description of the transaction",
    }

    response = requests.post(
        saf_stk_pushurl,
        json=push_data,
        headers=headers)

    return response.json()
