import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

url = "https://edition.cnn.com/business"
web_data = requests.get(url)

soup = BeautifulSoup(web_data.text, 'html.parser')
print(str(soup))
find_word = soup.find_all("span",{"class":"container__headline-text"},{"data-editable":"headline"})

'''
for i in find_word:
    #i = str(i).split('<span class="container__headline-text data-editable="headline">')
    #i = str(i).split('</span>')
    text = i.get_text()
    print(text)
    
''' 
headline_text = [
    h.get_text(strip=True)
    for h in find_word
]


df = pd.DataFrame(headline_text, columns=["Headlines"])
print(df)
#df.to_excel('bs4topicread_test.xlsx')
#Generate name of excel file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"newsreport_{timestamp}.xlsx"

#Create file
df.to_excel(filename, index=False)

print("Create file successfully")