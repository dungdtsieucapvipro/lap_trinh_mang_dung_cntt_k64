import requests
from bs4 import BeautifulSoup

response = requests.get('https://vnexpress.net')

if response.status_code == 200:
    soup = BeautifulSoup(response.content,'html.parser')
    title = soup.title.string

    print("Page Title:", title)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")