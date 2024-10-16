import requests
from bs4 import BeautifulSoup

response = requests.get('https://imgflip.com/memegenerator/124276589/Drake-NoYes')

if response.status_code == 200:
    soup = BeautifulSoup(response.content,'html.parser')
    title = soup.find("h1").get_text(strip=True)
    image = soup.find("img", class_= "im um")
    image_src = image['src'].replace("/2","",1)
    print(f"{title}:https:{image_src}")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")