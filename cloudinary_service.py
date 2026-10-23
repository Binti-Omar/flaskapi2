from dotenv import load_dotenv
import os
load_dotenv()
import cloudinary
import cloudinary.uploader
from send_email import email

cloud_name = os.getenv("CLOUD_NAME")
api_key = os.getenv("API_KEY")
secret_key = os.getenv("SECRET_key")

# connecting to cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("SECRET_key"),
)

def upload_pdf(pdf_file):
    try:
        file_path = f"receipts/{pdf_file}.pdf"
        # upload pdf
        upload = cloudinary.uploader.upload(file_path, resource_type = "raw" )
        receipt_url = upload["secure_url"]

        print("successful cloudinary upload")
        print(receipt_url)
        # send email
        email("chombobintiomar5@gmail.com","Payment received",f"Thank you we have received your payment.\n\n" f"Receipt: {receipt_url}")

        return "success"
    except Exception as e:
        print(f"upload failed: {e}")
    return "failed"

