import requests
import json
from bs4 import BeautifulSoup
import time

url = "https://disway.id/kategori/99/catatan-harian-dahlan/"

links = []  # Initialize an empty list to store the links

# Send an HTTP GET request to fetch the HTML content of the webpage

def get_links(links, url):
	response = requests.get(url)

	# Check if the request was successful
	if response.status_code == 200:
		# Parse the HTML content with BeautifulSoup
		soup = BeautifulSoup(response.text, 'html.parser')

		# Find all anchor tags within the specified div class ("bottom-15")
		link_divs = soup.find_all('h2', class_='media-heading')

		# Extract links from each div
		new_links = [div.find('a')['href'] for div in link_divs if div.find('a')]

		if links is None:
			links = []

		# Append new_links to links
		links.extend(new_links)
		
		return links


base_link = "https://disway.id/kategori/99/catatan-harian-dahlan/"


for denom in range(45):
	# if denom / 5 == 0:
	# 	time.sleep(3)
	angka = denom * 30

	# Use a conditional expression to handle the concatenation
	url_link = base_link + str(angka) if angka != 0 else base_link

	get_links(links, url_link)

print(links)

# Convert the links list into a dictionary with float keys
blog_map = {float(i+1): link for i, link in enumerate(links)}

print(blog_map)

# Save the blog_map dictionary into an updatable JSON file
json_file_path = 'blog_map.json'
with open(json_file_path, 'w') as f:
	json.dump(blog_map, f)

# Now you can read the JSON file and update the blog_map if needed
# Load the blog_map from the JSON file with keys converted back to float
def float_keys_hook(obj):
    return {float(key): value for key, value in obj.items()}

json_file_path = 'blog_map.json'
with open(json_file_path, 'r') as f:
    updated_blog_map = json.load(f, object_hook=float_keys_hook)

# You can now use the updated_blog_map dictionary with float keys as needed
print(updated_blog_map)

