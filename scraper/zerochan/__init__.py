import requests
import os
import re
from shutil import copyfileobj
from bs4 import BeautifulSoup
from requests.utils import add_dict_to_cookiejar
from urllib.request import Request, urlopen
from dotenv import set_key, find_dotenv, load_dotenv

from misc import *

SITE = "zerochan"

class ZerochanDownloader:
    def __init__(self, **params):
        self.params = params
        self.session = requests.Session()
        self.session.headers.update({"User-Agent" : UA})

        self.dl_dir = ""

    def inject_to_session(self):
        load_dotenv(find_dotenv())

        zhash = self.params['z_hash'] if self.params['z_hash'] != "" else os.getenv("z_hash")
        zid = self.params['z_id'] if self.params['z_id'] != "" else os.getenv("z_id")   

        if self.params.get("z_hash"):
            add_dict_to_cookiejar(self.session.cookies, {"z_hash" : zhash, "z_id" : zid})

            if self.params['save'] == True:
                set_key(find_dotenv(), "z_hash", self.params['z_hash'])
                set_key(find_dotenv(), "z_id", self.params['z_id'])
                
    def download_content(self, url, post_id, extension):
        filename = f"{post_id}.{extension}"

        if not os.path.exists(self.dl_dir + f"\\{filename}"):
            try:
                with urlopen(url) as response, open(self.dl_dir + f"\\{filename}", "wb") as contentfile:
                    copyfileobj(response, contentfile)
            except:
                log("ERROR", f"Unable to download {filename}")
                exit()

            log("INFO", f"Downloaded {filename}")

    def get_post_container(self, url):
        page_req = self.session.get(url).content
        soup = BeautifulSoup(page_req, "lxml")

        try:
            return soup.find("ul", id = "thumbs2").find_all("li")
        except:
            log("ERROR", "Container for posts not found")
            exit()
        
    def check_page_post(self, post):
        favorites = int(post.find("a", class_ = "fav").text)

        if favorites >= self.params['min_score']:
            return True

        else:
            log("WARN", "Post bypassed qualification. Skipped")
            return False

    def get_post_url(self, url):
        post_req = self.session.get(url).content
        post_soup = BeautifulSoup(post_req, "lxml")

        try: 
            return post_soup.find("div", id = "large").find("a", class_ = 'preview')['href']

        except:
            log("ERROR", "Unable to retrive image url")
            exit()

    def verify_url(self, url):
        if SITE.lower() not in url:
            log("ERROR", "Given URL is invalid")
            exit()
            
    def download(self, url):
        log("INFO", "Starting session...")

        self.inject_to_session()

        self.verify_url(url)

        self.dl_dir = init_download_dir(SITE)
        
        if url == "https://www.zerochan.net":
            posts = self.get_post_container(url)

            for post in posts:
                if self.check_page_post(post):
                    url = self.get_post_url(f"https://zerochan.net{post.find('a', class_ = 'thumb')['href']}")

                    self.download_content(url, post['data-id'], url.split(".")[-1])

        else:
            if "?p=" in url:
                start_page = int(re.search(r"p=(\d+)\b", url).group(1))

            else:
                start_page = 1
                url = url + "&p=" + str(start_page) if "?" in url else url + "?p=" + str(start_page)

            max_page = self.params['pages']

            for page in range(start_page, start_page + max_page):
                log("INFO", f"Current page ID [{page}]")
                url = url.replace("p=" + re.search(r"p=(\d+)\b", url).group(1), "p=" + str(page))

                posts = self.get_post_container(url)

                for post in posts:
                    if self.check_page_post(post):
                        post_url = self.get_post_url(f"https://www.zerochan.net{post.find('a', class_ = 'thumb')['href']}")

                        self.download_content(post_url, post['data-id'], post_url.split(".")[-1])

        log("INFO", "Session concluded. Check for your downloads!")
        exit()