import requests
from bs4 import BeautifulSoup

# URL of the blog post
url = 'https://disway.id/read/705670/teflon-luhut'
urls = [
    'https://disway.id/read/686230/geothermal',
    'https://disway.id/read/708137/aceh-only',
    'https://disway.id/read/705670/teflon-luhut'
]

# Send a GET request to the URL and retrieve the HTML content
response = requests.get(url)
html_content = response.content

# Create a BeautifulSoup object to parse the HTML
article = BeautifulSoup(html_content, 'html.parser')

# Extract the title
title = article.find('h1', class_='text-black').text.strip()


# Extract the main content
# main_content = soup.find('div', class_='entry-content').text #.strip()

main_content = article.find(class_='post') 
# Extract the main image
imgs = main_content.findAll('img') #, class_='img-responsive').get('src')

# Print the extracted information
print('Title:', title)
print('Main Content:', main_content)
print("separatorrr")
print(imgs)
