import requests
import os
import re
from urllib.request import urlopen, Request
from shutil import copyfileobj
from bs4 import BeautifulSoup

from ...misc import *

SITE = "Gelbooru"

class GelbooruDownloader:
    def __init__(self, **params):
        self.params = params
        self.session = requests.Session()

        self.dl_dir = init_download_dir(SITE)

    def download_content(self, url, post_id, extension):
        filename = f"{post_id}.{extension}"

        if not os.path.exists(self.dl_dir + f"\\{filename}"):
            to_open = Request(url)
            to_open.add_header("User-Agent", UA)

            try:
                with urlopen(to_open) as response, open(self.dl_dir + f"\\{filename}", "wb") as contentfile:
                    copyfileobj(response, contentfile)

            except:
                log("WARN", f"Unable to download {filename}")

            log("INFO", f"Downloaded {filename}")

    def check_page_post(self, post):
        try:
            image_element = post.find("img")

            title = image_element['title']
            score = int(re.search(r"score:(.*)\ ", title).group(1).strip())
            rating = re.search(r"rating:(.*)", title).group(1)[0].lower().strip() # Gets the leading character of rating: q e s g

            if rating in self.params['ratings'] and score >= self.params['min_score']:
                if self.params['scope'] == 'img':
                    if 'video' not in title or 'animated' not in title:
                        return True

                    else:
                        return False

                return True

            else:
                log("WARN", "Post bypassed qualification. Skipped")
                return False

        except:
            log("ERROR", "Unable to qualify post")
            exit()

    def get_post_container(self, url):
        page_req = self.session.get(url).content
        soup = BeautifulSoup(page_req, "lxml")

        try:
            return soup.find("div", class_ = "thumbnail-container").find_all("article")
            
        except:
            log("ERROR", "Container for posts not found")
            exit()
    
    def parse_post(self, url):
        post = {}

        post_req = self.session.get(url).content
        post_soup = BeautifulSoup(post_req, "lxml")

        try:
            post['id'] = [x.text for x in post_soup.find_all("li") if x.text.__contains__("Id")][0].split(":")[-1].strip()
            post['url'] = [x for x in post_soup.find_all("li") if x.text == "Original image"][0].find("a")['href']

        except:
            log("ERROR", "Unable to parse post")
            exit()
            
        return post

    def download(self, url):
        log("INFO", "Session starting...")

        start_page = int(re.search(r"\&pid=(.*)", url).group(1)) if "&pid=" in url else 0
        max_page = start_page + (self.params['pages'] * 42)

        for page in range(start_page, max_page, 42):
            log("INFO", f"Current page ID [{page}]")

            for post in self.get_post_container(url if '&pid=' in url else url + "&pid=" + str(page)):
                if self.check_page_post(post):
                    parse_post = self.parse_post(post.find('a')['href'])

                    self.download_content(parse_post['url'], parse_post['id'], parse_post['url'].split(".")[-1])

        log("INFO", "Session ended. Check the destination path!")
        exit()