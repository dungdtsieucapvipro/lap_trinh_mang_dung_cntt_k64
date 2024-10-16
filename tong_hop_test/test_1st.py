import requests
response = requests.get("https://vnexpress.net")

print(response.content)
