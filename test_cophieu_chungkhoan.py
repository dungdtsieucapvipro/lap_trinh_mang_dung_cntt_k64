from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://eoddata.com/stocklist/NASDAQ/A.htm"
res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml')  # Chỉ định parser 'lxml'

data = []
for row in soup.select('#ctl00_cph1_divSymbols table tr:has(td)'):
    d = dict(zip(soup.select_one('#ctl00_cph1_divSymbols table tr:has(th)').stripped_strings, row.stripped_strings))
    d.update({'url': 'https://eoddata.com' + row.a.get('href')})
    data.append(d)

# Tạo DataFrame
df = pd.DataFrame(data)
print(df)
