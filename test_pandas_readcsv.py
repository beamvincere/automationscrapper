import pandas as pd
import numpy as np
import glob
import os
from io import StringIO

#df = pd.read_csv('data.csv', index_col=0)
#df = pd.read_excel('data.xlsx', index_col=0)
#df = pd.read_json('data.json')
#df = pd.read_html('data.html')

#Read lastest excel file
#Find all excel files matching patter
files = glob.glob("newsreport_*.xlsx")

#Get lastest file
lastes_file = max(files, key=os.path.getmtime)

df = pd.read_excel(lastes_file)

print(df)
print(str(lastes_file))