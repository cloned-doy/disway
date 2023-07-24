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
soup = BeautifulSoup(html_content, 'html.parser')

# Extract the title
title = soup.find('h1', class_='text-black').text.strip()

# Extract the date post
date_post = soup.find('span', class_='date').text.strip()

# Extract the author
author = soup.find('div', class_='author').strong.text.strip()

# Extract the main image
main_image = soup.find('img', class_='img-responsive').get('src')

# Extract the main content
# main_content = soup.find('div', class_='entry-content').text #.strip()

main_content = soup.find('div', class_='text-grey').text #.strip()

# Print the extracted information
print('Title:', title)
print('Date Post:', date_post)
print('Author:', author)
print('Main Image:', main_image)
print('Main Content:', main_content)


# # Parse the HTML content
# soup = BeautifulSoup(main_content, 'html.parser')

# # Extract main content
# main_content = soup.find('div', class_='post').get_text()

# # Extract image URL if available
# image_content = soup.find('img')['src'] if soup.find('img') else None

# # Extract author name
# author_name = soup.find('div', id='author').strong.get_text()

# # Print the results
# print("Main Content:")
# print(main_content.strip())

# if image_content:
#     print("\nImage URL:")
#     print(image_content)

# print("\nAuthor Name:")
# print(author_name.strip())
