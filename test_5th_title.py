import requests
from bs4 import BeautifulSoup

response = requests.get('https://imgflip.com/memetemplates?page=1')

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    titles = soup.find_all("h3")  # Tìm tất cả các thẻ <h3>
    
    for title in titles:  # Duyệt qua từng thẻ <h3>
        print(title.get_text(strip=True))  # Lấy và in văn bản bên trong thẻ <h3>
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
