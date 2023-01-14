import requests
from bs4 import BeautifulSoup

url = "https://www.google.com/search?q=thrasio+acquires&oq=thrasio+acquires&aqs=chrome..69i57j0i512j0i22i30.3589j0j1&sourceid=chrome&ie=UTF-8#ip=1"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract all links from the page
links = [a['href'] for a in soup.find_all('a', href=True) if a.text]

# Filter out links that are not to articles
articles = [link for link in links if '/url?q=' in link]

# remove the /url?q= part
articles = [link.replace('/url?q=', '') for link in articles]

with open('text.txt', 'w') as f:
    f.write('\n\n'.join(articles) + '\n')