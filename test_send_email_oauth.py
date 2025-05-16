import smtplib
import os
import base64
import mimetypes
import pandas as pd
import glob
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

#Access token with OAuth
SCOPES = ["https://mail.google.com/"]
CLIENT_SECRET_FILE = "credentials1.json"

def get_credentials():
    creds = None
    token_file = "token.json"
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        #Save Token
        with open(token_file, "w") as token:
            token.write(creds.to_json())
    return creds

#Create XOAuth2 String and pass through SMTP
def send_email_with_oauth2(creds):
    access_token = creds.token
    #email_address = creds._id_token["email"]
    email_address = "testerpywebscrapping@gmail.com"
    auth_string = f"user={email_address}\x01auth=Bearer {access_token}\x01\x01"
    auth_string = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")

    msg = EmailMessage()
    msg["Subject"] = "Sending test email mini web scrapper"
    msg["From"] = email_address
    msg["To"] = "testsending_1@outlook.com"
    msg.set_content("This email for testing sent text and file news report with python automation using Gmail SMTP with OAuth2.0 !!")

    #Read lastest file of excel file
    files = glob.glob("newsreport_*.xlsx")
    lastest_files = max(files, key=os.path.getmtime)
    print(str(lastest_files))

    #Excel file attachment
    excel_file = lastest_files
    if os.path.exists(excel_file):
        with open(excel_file, "rb") as f:
            file_data = f.read()
            mime_type, _ , = mimetypes.guess_type(excel_file)
            maintype, subtype = mime_type.split("/")
            msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=os.path.basename(excel_file))
    else:
        print(f"Excel file not found: {excel_file}")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.docmd("AUTH", f"XOAUTH2 {auth_string}")
            smtp.send_message(msg)
            print("Email sent successfully")
    except Exception as e:
        print(f"Error: {e}")

#Run Program and funtion
if __name__ == "__main__":
    creds = get_credentials()
    print(creds._id_token)
    send_email_with_oauth2(creds)
