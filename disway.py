import requests
from bs4 import BeautifulSoup
from ebooklib import epub

# List of URLs for the blog posts
urls = [
    'https://disway.id/read/686230/geothermal',
    'https://disway.id/read/708137/aceh-only',
    'https://disway.id/read/705670/teflon-luhut'
]

# Create a new EPUB book
book = epub.EpubBook()
book.set_title('Blog Posts')
book.add_author('Your Name')

# Loop through the URLs
for index, url in enumerate(urls):
    # Send a GET request to the webpage
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)

    # Extract the title and content from the webpage
    title = soup.find('h1').text.strip()
    print(title)
    content = soup.find('article')
    print(content)

    # Create a new chapter
    chapter_file_name = f'chapter_{index + 1}.xhtml'
    chapter = epub.EpubHtml(title=title, file_name=chapter_file_name, lang='en')

    # Add text content to the chapter
    chapter.set_content(content.prettify())

    # Extract and add images to the chapter
    images = content.find_all('img')
    for i, image in enumerate(images):
        image_url = image['src']
        image_data = requests.get(image_url).content
        image_name = f'image_{index + 1}_{i + 1}.jpg'
        chapter.add_item(epub.EpubItem(uid=f'img_{index + 1}_{i + 1}', file_name=image_name, media_type='image/jpeg', content=image_data))
        chapter.content = chapter.content.replace(image_url, image_name)

    # Add the chapter to the book
    book.add_item(chapter)
    book.spine.append(chapter)

# Save the EPUB file
epub.write_epub('output.epub', book, {})

print('EPUB file created successfully.')
