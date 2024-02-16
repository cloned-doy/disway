import requests
import json
from bs4 import BeautifulSoup
from time import sleep

#fetch the HTML content of the base url and get all the blog post links
def get_links(links, base_url):

	if links is None: links = []
	response = requests.get(base_url)

	if response.status_code == 200:
		soup = BeautifulSoup(response.text, 'html.parser')

		# Find all anchor tags within the specified div class ("bottom-15")
		link_divs = soup.find_all('h2', class_='media-heading')
		new_links = [div.find('a')['href'] for div in link_divs if div.find('a')]
		links.extend(new_links)
		
		print(f"total new links: {len(links)}")
	
	return links
	

def main(base_url, page_total, blog_map_path):

	print("base url: "+base_url)
	print("start getting the post links")

	links = []  # Initialize an empty list to store the links
	for denom in range(page_total):
		post_id = denom * 30 # 30 is the default total post of each page
		url_link = base_url + str(post_id) if post_id != 0 else base_url # Use a conditional expression to handle the concatenation
		get_links(links, url_link)
		# if denom / 10 == 0 : sleep(30) # dumb line to make the requests fecth block safe

	# Convert the links list into a dictionary with float keys
	blog_map = {float(i+1): link for i, link in enumerate(links)}

	# Save the blog_map dictionary into an updatable JSON file
	with open(blog_map_path, 'w') as f:
		json.dump(blog_map, f)
		
	print("link gathering is done.")
	# print(blog_map)
	print(f"total links: {len(links)}")

if __name__ == "__main__":

	base_url = "https://disway.id/kategori/99/catatan-harian-dahlan/" # base url disway
	page_total = 76 # total page of disway blog. per page is 30 posts
	blog_map_path = "blog_map.json" # json to save blog post links

	main(base_url, page_total, blog_map_path)