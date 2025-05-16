from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import smtplib
import os
import base64
import mimetypes
import glob
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


#Create web driver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

#Get website
driver.get("https://www.lazada.co.th/#?")

time.sleep(5)
#Insert website
'''
langguage_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="modal"]/div[1]/div[1]/div/div[3]/div[2]/button'))
)
langguage_button.click()
'''
#Find product lazada website
try:
    search_product = driver.find_element(By.XPATH, '//*[@id="q"]')
    search_product.send_keys("เสื้อแจ็กเก๊ตยีนส์ mc")
    print("Search product already")

    search_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="topActionHeader"]/div/div[2]/div/div[2]/div/form/div/div[2]/a'))
    )
    search_btn.click()
    print("On product search")
except Exception as e:
    print(f"Error details: {e}")

#Zoom out process
#driver.execute_script("document.body.style.MozTransform='scale(0.1)';")
#driver.execute_script('document.body.style.MozTransformOrigin = "0 0";')


'''
page_data = driver.page_source
page_soup = BeautifulSoup(page_data, 'html.parser')
page_lenght = page_soup.find_all("li",{"class":"ant-pagination-item"})
page = len(page_lenght)-2
print(page)
'''

all_inform = []
for i in range(2):
    try:
        print("Start scraping data on website page")
        data = driver.page_source
        soup = BeautifulSoup(data, 'html.parser')
        product_title = soup.find_all("div",{"class":"buTCk"})
        print(f"Column product:{len(product_title)}")
            
        for p in product_title:
            product_name = p.find("div", {"class":"RfADt"}).text
            product_price = p.find("span", {"class":"ooOxS"}).text
            product_sold = p.find("span", {"class":"_1cEkb"}).text if p.find("span", {"class":"_1cEkb"})else'N/A'
            product_location = p.find("span", {"class":"oa6ri"}).text
            #print(f"Product name: {product_name} | Price: {product_price} | Sold: {product_sold}")
            inform_data = [product_name, product_price, product_sold, product_location]
            all_inform.append(inform_data)
            #print(all_inform)
        

    except Exception as e:
        print(f"Error details: {e}")

    time.sleep(5)
    next_button = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[3]/div/ul/li[9]/button')
    next_button.click()
    time.sleep(5)


df = pd.DataFrame(all_inform, columns=['Product', 'Price', 'Sold', 'Loction product'])
print(df)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"lazadareport_{timestamp}.xlsx"

#Create file
df.to_excel(filename, index=False)

print("Create file successfully")

#Email sending Process
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
    files = glob.glob("lazadareport_*.xlsx")
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


