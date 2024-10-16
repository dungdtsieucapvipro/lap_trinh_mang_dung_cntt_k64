import requests
from bs4 import BeautifulSoup

response = requests.get('https://imgflip.com/memetemplates?page=1')

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    danh_sach_A = soup.findAll("a",class_="mt-caption")
    for tag_a in danh_sach_A:
        full_href = 'https://imgflip.com/' + tag_a['href']
        print(full_href)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")