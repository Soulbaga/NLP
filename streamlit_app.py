sudo pip install requests

import requests


url = "https://www.google.com/search?q=hello+world"

response = requests.get(url)

print(response.text)
