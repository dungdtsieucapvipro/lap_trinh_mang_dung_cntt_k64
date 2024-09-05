import requests
from bs4 import BeautifulSoup

response = requests.get('https://vnexpress.net/bao-yagi-manh-len-cap-15-4789136.html')

if response.status_code == 200:
    soup = BeautifulSoup(response.content,'html.parser')
    article_tag = soup.find('article')
    article_date = soup.find("span", class_= "date")
    title = soup.find("h1", class_= "title-detail").get_text(strip=True)
    if article_date:
        date = article_date.get_text(strip=True)
    if article_tag:
        article_content = article_tag.get_text(strip=True)
        with open('article_content.txt', 'w', encoding='utf-8') as file: 
            file.write(title +"\n")
            file.write(date +"\n")
            file.write(article_content)
    else:
        print("No <article> tag found.")
    
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")