import smtplib as smtp
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

#Environment
email_sender = 'testsending_1@outlook.com'
email_password = 'UZF5V-WKA5U-NKTQR-A4HRU-32JSR'
email_receiver = 'suphawichprakobnan@gmail.com'


#Inform in email
msg = MIMEMultipart()
msg['From'] = email_sender
msg['To'] = email_receiver
msg['Subject'] = 'Hello first python sending email'

body = """ 
Hi this email sent testing scrip automation

thanks
The eng
"""
msg.attach(MIMEText(body, 'plain'))


#File insert
''''
filename = ""
try:
    with open(filename, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename = {filename}')
        msg.attach(part)
except:
    print(f"File not found or cannot insert file")
'''

#Email sending
try:
    server = smtp.SMTP('smtp-mail.outlook.com', 587)
    #status_code, response = smtp.ehlo()
    #print(f"[*] Echoing the server: {status_code} {response}")
    server.starttls()
    server.login(email_sender, email_receiver)
    text = msg.as_string
    server.sendmail(email_sender, email_receiver, text)
    print("Email sent")
except Exception as e:
    print(f"Error: {e}")
finally:
    server.quit()