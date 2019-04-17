#import libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup

#specify url
url = 'args.website'

page = requests.get(url)
page.text

#parse html
soup = BeautifulSoup(page.text, 'html.parser')

#read text to summarize
text = []

text_p = soup.find_all(class_="content-text")

for item in text_p:
    text.append(item.text)
    
    
print(text)