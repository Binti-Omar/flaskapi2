from dotenv import load_dotenv
import os
load_dotenv()

import mailtrap

mailtrap_token=os.getenv("MAILTRAP_TOKEN")

def email(to,subject,message):
    mail = mailtrap.Mail(
        sender = mailtrap.Address(email = "hello@demomailtrap.co",name = "FLASK_API2"),
        to = [mailtrap.Address(email = to)],
        subject = subject, 
        text = message,
        category = "mailtrap integration test"
    )
    client = mailtrap.MailtrapClient(token = mailtrap_token)
    response = client.send(mail)

    print("this is mailtrap---------------------------------------")
    print(response)

# email("chombobintiomar5@gmail.com","Testing API","I am testing my API")