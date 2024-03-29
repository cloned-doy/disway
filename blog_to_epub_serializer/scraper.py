import logging
import os
import time
from pathlib import Path
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup
from ebooklib import epub

from blog_to_epub_serializer.book_utils import Chapter, Book

logger = logging.getLogger("scraper")
logging.basicConfig(
    level=logging.INFO,
    # level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

LOCAL_CACHE = f"local_cache"


class Scraper:
    # directories in relation to repo base
    SCRAPER_CACHE = LOCAL_CACHE

    def __init__(
        self,
        title: str,
        author: str,
        blog_map: Dict[float, str],
        epub_name: str,
        cover_img_path: Optional[str] = None,
    ):
        # used in the epub metadata
        self.title = title
        # used in the epub metadata
        self.author = author

        # dictionary of chapter numbers (float) to html paths
        self.blog_map = blog_map
        # the local file name that will be created
        self.epub_name = epub_name

        # this should be the local path of the image
        self.cover_img_path = cover_img_path

    def run(self, use_cache: bool = True) -> None:
        """
        Start the scraper. Will grab all html + image files, then process and
        save them into an epub.

        :param  use_cache:  whether to pull everything fresh from the internet
                            or use locally downloaded files

                do_precook: bool = True (opt for next dev.)
        """

        # do precook first. it will make the soup cooking experience feel better 
        request_counter = 0  
        for key, url in self.blog_map.items():
            logger.info(f"Preparing {key} at url {url}")
            soup = None
            if use_cache:
                try:
                    soup = self.read_soup_from_file(key)
                    logger.info(f"Loaded cached file for {key}")
                except FileNotFoundError:
                    # if local file not found, then look for
                    logger.warning(
                        f"Could not find a file for {key}, fetching from web"
                    )
                    pass
            if not use_cache or not soup:
                
                request_counter += 1
                if request_counter % 150 == 0:
                    # Add a sleep of 150 seconds after every 150 requests
                    logger.info("150 requests reached. Sleep for 150 secs...")
                    time.sleep(150)
                    request_counter = 0  # Reset the counter after the sleep

                # soup = self.fetch_page(url, key)
                self.fetch_page(url, key)


        # now lets cook the soup
        chapters = []
        preface_chapters = self.add_preface_chapters()
        if preface_chapters:
            chapters = preface_chapters

        for key, url in self.blog_map.items():
            logger.info(f"Checking {key}")
            soup = None

            try:
                soup = self.read_soup_from_file(key)
                logger.info(f"Loaded on {key}")
            except FileNotFoundError:
                # if local file not found, then look for
                # retry to fetch from web for one last time
                soup = self.fetch_page(url, key)
                logger.warning(
                    f"Its serious now. A page was totally failed to load. The {key} skipped."
                )
                pass

            try:
                chapter = self.parse_chapter_text(soup, key)
                chapters.append(chapter)
            except:
                logger.warning(f"Ada error di retrieving post")
                pass

        book = Book(
            self.title,
            self.author,
            cover_img_path=self.cover_img_path,
            chapters=chapters,
        )
        book.finish_book()

        # save book to file
        epub.write_epub(f"{LOCAL_CACHE}/{self.epub_name}", book.ebook, {})

    def soup_precook():
        """in large size pages, prepare the soup first before put one by one in the plate"""
        pass

    @classmethod
    def read_soup_from_file(
        cls,
        key: float,
    ) -> BeautifulSoup:
        """
        Given the chapter key, fetch the saved html

        :param key: the chapter number page to retrieve
        :return: html/beautifulsoup loaded page
        """
        with open(f"{cls.SCRAPER_CACHE}/soup_{key}.html", "r") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        return soup

    @classmethod
    def fetch_page(cls, url: str, key: float) -> BeautifulSoup:
        """
        Fetch the page from url and save to the SOUP_DIR

        :param url: the blog page that contains the chapter to ingest
        :param key: the chapter number this page represents
        :return: html/beautifulsoup loaded page
        """
        # confirm the directory exists, creating any intermediates required
        if not os.path.exists(cls.SCRAPER_CACHE):
            os.makedirs(cls.SCRAPER_CACHE)
            logger.info(f"Created directory path {cls.SCRAPER_CACHE}")

        response = requests.get(url)
        with open(f"{cls.SCRAPER_CACHE}/soup_{key}.html", "w") as f:
            f.write(response.text)

        return BeautifulSoup(response.text, "html.parser")

    def parse_chapter_text(
        self, soup: BeautifulSoup, chapter_idx: float
    ) -> Chapter:
        """
        Method to parse the beautiful soup and edit its contents.  Should
        also save any desired images to local storage
        (use self.fetch_and_save_img)

        :param soup: the html soup to parse and edit
        :param chapter_idx: the chapter number this soup represents
        :return: the Chapter ready to be added to the Book
        """
        raise NotImplementedError()

    def add_preface_chapters(self) -> Optional[List[Chapter]]:
        """
        An optional method to add chapters to the beginning of the book.
        The implementor is responsible for creating or parsing html.
        Should be implemented in subclasses and return a Chapter
        """

    @classmethod
    def fetch_and_save_img(cls, src: str, key: Optional[float] = None) -> str:
        """
        Given an image url, download and save the file to local storage.

        :param src: url source of the image to be downloaded and saved
        :param key: the chapter this image relates to. (this is used to prevent
            multiple images sharing the same name across different chapters)
        :return: the local path the image was downloaded to
        """
        # determine the full directory path, if supplied a key
        directory = cls.SCRAPER_CACHE
        if key:
            directory = f"{directory}/{key}"

        # confirm the directory exists, creating any intermediates required
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created directory path {directory}")

        filename = src.split("/")[-1]
        full_file_path = f"{directory}/{filename}"
        # if a file does not already exist at the name designated
        # - download and store it
        # if a file does not already exist at the name designated
        # - download and store it
        if not os.path.isfile(full_file_path):
            logger.info(
            f"Could not find file {full_file_path}. Fetching from web."
            )
            retries = 3  # Number of retries
            delay = 3  # Delay between retries in seconds

            for i in range(retries):
                try:
                    file = requests.get(src)
                    with open(full_file_path, "wb") as f:
                        f.write(file.content)
                    return full_file_path
                except requests.exceptions.ConnectionError as e:
                    if i < retries - 1:
                        logger.warning(f"Retry {i + 1} of {retries} failed. Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        logger.error("Failed to fetch the image after multiple retries.")
                        raise e
        else:
            logger.info(f"Image already exists at {full_file_path}. Skipping download.")
            return full_file_path