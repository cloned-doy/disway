from typing import Dict
import json

from bs4 import BeautifulSoup

from blog_to_epub_serializer.book_utils import Chapter
from blog_to_epub_serializer.scraper import Scraper, LOCAL_CACHE
   
class Disway(Scraper):
    SCRAPER_CACHE = f"{LOCAL_CACHE}/disway"

    def parse_chapter_text(
        self, soup: BeautifulSoup, chapter_idx: float
    ) -> Chapter:

        # Create a BeautifulSoup object to parse the HTML
        # Extract the title
        chapter_title = soup.find('h1', class_='text-black').text.strip()

        chapter_content = soup.find(class_='post')

        # Extract the main image
        img_blocks = chapter_content.findAll('img') #, class_='img-responsive').get('src')
        local_srcs = []
        for img in img_blocks:
            local_src = self.fetch_and_save_img(
                img["src"], chapter_idx
            )
            img["src"] = local_src
            local_srcs.append(local_src)

        return Chapter(
            idx=chapter_idx,
            title=chapter_title,
            html_content=chapter_content,
            image_paths=local_srcs,
        )


# Now you can read the JSON file and update the blog_map if needed
# Load the blog_map from the JSON file with keys converted back to float
def float_keys_hook(obj):
    return {float(key): value for key, value in obj.items()}

json_file_path = 'blog_map.json'
with open(json_file_path, 'r') as f:
    blog_map = json.load(f, object_hook=float_keys_hook)

title = "Harian Disway"
author = "Dahlan Iskan"
cover_img_path = f"{LOCAL_CACHE}/abah.jpg"
# cover_img_path = None
epub_name = "Harian Disway.epub"

scraper = Disway(
    title=title,
    author=author,
    cover_img_path=cover_img_path,
    blog_map=blog_map,
    epub_name=epub_name,
)

scraper.run()
