import requests
import os
import re
from urllib.request import urlopen, Request
from shutil import copyfileobj
from bs4 import BeautifulSoup

from ...misc import *

SITE = "Danbooru"

class DanbooruDownloader:
    def __init__(self, **params):
        self.params = params
        self.session = requests.Session()

        self.dl_dir = init_download_dir(SITE)

    def download_content(self, url, post_id, extension):
        filename = f"{post_id}.{extension}"

        if not os.path.exists(self.dl_dir + f"\\{filename}"):
            try:
                with urlopen(url) as response, open(self.dl_dir + f"\\{filename}", "wb") as contentfile:
                    copyfileobj(response, contentfile)

                log("INFO", f"Downloaded {filename}")

            except:
                log("WARN", f"Unable to download {filename}")

    def check_page_post(self, post):
        if post['data-rating'].strip() in self.params['ratings'] and int(post['data-score']) >= self.params['min_score']:
            if self.params['scope'] == "img":
                if "video" not in post['data-tags'] or "animated" not in post['data-tags']:
                    return True
                        
                else:
                    return False

            return True

        else:
            log("WARN", "Post bypassed qualification. Skipped")
            return False

    def inject_input_url(self, url, page):
        try:
            if "?page=" not in url:
                if "?d=" in url:
                    url = url.replace(re.search(r"\bd=(\d+)(&)", url).group(1), "1&page=" + str(page))
                
                else:
                    url = url.replace(re.search(r"\bpage=(/d+)(&|$)", url).group(1), str(page))
            else:
                url = url.replace(re.search(r"\bpage=(\d+)(&|$)", url).group(1), str(page))

            return url

        except:
            log("ERROR", "Unable to parse URL")
            exit()

    def get_post_container(self, url):
        page_req = self.session.get(url).content
        soup = BeautifulSoup(page_req, "lxml")

        try:
            return soup.find("div", class_ = re.compile("posts-container")).find_all("article")

        except:
            log("ERROR", "Container for posts not found")
            exit()

    def parse_post(self, url):
        post = {}

        post_req = self.session.get(url).content
        post_soup = BeautifulSoup(post_req, "lxml")

        try:
            post_info = post_soup.find("section", id = "post-information").find("ul")
            post['id'] = post_info.find("li", id = "post-info-id").text.split(" ")[-1]
            post['url'] = post_info.find("li", id = "post-info-size").find("a")['href']

        except:
            log("ERROR", "Unable to parse post")
            exit() 
            
        return post

    def download(self, url):
        log("INFO", "Session starting...")

        start_page = re.search(r"\bpage=(\d+)(&|$)", url)

        if not start_page:
            start_page = 1
        else:
            start_page = int(start_page.group(1))

        max_page = self.get_max_page(start_page)

        for page in range(start_page, max_page):
            log("INFO", f"Current page ID [{page}]")

            injected_url = url.replace(re.search())
            for post in self.get_post_container(self.inject_input_url(url, page)):
                if self.check_page_post(post):
                    parse_post = self.parse_post(f"https://danbooru.donmai.us{post.find('a')['href']}")

                    self.download_content(parse_post['url'], parse_post['id'], parse_post['url'].split(".")[-1])

        log("INFO", "Session ended. Check the destination path!")
        exit()