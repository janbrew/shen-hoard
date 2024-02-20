import requests
import os
import re
from shutil import copyfileobj
from urllib.request import urlopen
from bs4 import BeautifulSoup

from ..misc import *

SITE = "Yandere"

class YandereDownloader:
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

            except: 
                log("WARN", f"Unable to download {filename}")
                
            log("INFO", f"Downloaded {filename}")

    def check_page_post(self, post):
        try:
            image_element = post.find("img")
            title = image_element['title']

            rating = re.search(r"Rating:(.*)\ ", title).group(1).lower().strip().split(" ")[0][0]
            score = int(re.search(r"Score:(.*)\ ", title).group(1).strip().split(" ")[0])

            if rating in self.params['ratings'] and score >= self.params['min_score']:
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
            return soup.find("div", id = "content").find("div").find("div", class_ = "content").find("ul").find_all("li")

        except:
            log("ERROR", "Container for posts not found")
            exit()

    def get_post_url(self, post):
        post_req = self.session.get(post).content

        soup = BeautifulSoup(post_req, "lxml")

        try:
            sidebar = soup.find("div", class_ = "sidebar").find_all("div")

            for div in sidebar:
                for li in div.find_all("li"):
                    try:
                        url = li.find('a', id = 'highres')['href']
                    except:
                        continue
                    return url

        except:
            log("ERROR", "Unable to retrieve post url")
            exit()

    def download(self, url):
        log("INFO", "Session starting")

        start_page = re.search(r"\bpage=(\d+)(&|$)", url)

        if not start_page:
            start_page = 1
        else:
            start_page = int(start_page.group(1))

        max_page = start_page + self.params['pages']

        for page in range(start_page, max_page):
            log("INFO", f"Current page ID [{page}]")

            injected_url = re.search(r"\bpage=(\d+)(&|$)", url)

            if injected_url:
                url.replace(injected_url, str(page))
            else:
                if "?tags" in url:
                    url.replace("post?", "post?page=" + str(page))
                else:
                    url = url + "?page=" + str(page)

            for post in self.get_post_container(url):
                if self.check_page_post(post):
                    post_href = f'https://yande.re{post.find("div").find("a")["href"]}'
                    content_url = self.get_post_url(post_href)

                    self.download_content(content_url, post['id'][1:], content_url.split(".")[-1])

            log("INFO", "Session ended. Check the destination path!")
            exit()
