import requests
import os
import re
import string
import shutil
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from requests.utils import add_dict_to_cookiejar
from shutil import copyfileobj
from dotenv import load_dotenv, find_dotenv, set_key
from PIL import Image

from misc import *

SITE = "nHentai"

class nHentaiDownloader:
    def __init__(self, **params):
        load_dotenv(find_dotenv())

        self.params = params
        self.session = requests.Session()

        self.dl_dir = ""

    def inject_to_session(self):
        clearance = self.params['clearance'] if self.params['clearance'] != "" else os.getenv("CF_CLEARANCE")
        token = self.params['token'] if self.params['token'] != "" else os.getenv("CSRFTOKEN")

        self.session.headers.update({"User-Agent" : UA})
        add_dict_to_cookiejar(self.session.cookies, {"cf_clearance" : clearance, "csrftoken" : token})

        if self.params['save'] == True:
            set_key(find_dotenv(), "CF_CLEARANCE", self.params['clearance'])
            set_key(find_dotenv(), "CSRFTOKEN", self.params['token'])

    def parse_doujin(self, url):
        log("INFO", "Getting doujin details")

        doujin = {}

        doujin_req = self.session.get(url).content
        soup = BeautifulSoup(doujin_req, "lxml")

        try:
            info_block = soup.find("div", id = "info-block")
            doujin['title'] = "".join([c for c in info_block.find("h1").find("span", class_ = "pretty").text if c in string.ascii_letters + string.digits + " "]).strip()
            doujin['id'] = info_block.find("h3").text[1:]
            doujin['pages'] = int(info_block.find_all("div", class_ = re.compile(r"tag-container"))[-2].find("span").text)

        except:
            log("ERROR", "Unable to parse doujin")
            exit()

        return doujin

    def get_page_image_url(self, url):
        page_req = self.session.get(url).content
        soup = BeautifulSoup(page_req, "lxml")

        try:
            container = soup.find("section", id = "image-container")
            image = container.find("img")['src']

        except: 
            log("ERROR", "Unable to retrieve page image url")
            exit()

        return image
    
    def download_content(self, doujin, current_page, url, images):
        request = Request(url)
        request.add_header("User-Agent", UA)

        doujin_path = f"{doujin['id']} - {doujin['title']}"
        filename = f"{current_page}.png"
        image_path = self.dl_dir + f"\\{doujin_path}\\{filename}"

        os.mkdir(self.dl_dir + f"\\{doujin_path}") if not os.path.exists(self.dl_dir + f"\\{doujin_path}") else None

        try:
            with urlopen(request) as response, open(image_path, "wb") as pagefile:
                copyfileobj(response, pagefile)

        except:
            log("ERROR", f"Unable to download {filename}")
            exit()

        images.append(Image.open(image_path))
        log("INFO", f"Downloaded page {current_page}")

    def convert_to_pdf(self, doujin, images):
        try:
            images[0].save(
                self.dl_dir + f"\\{doujin['id']} - {doujin['title']}.pdf", resolution = 100.0, save_all = True, append_images = images[1:]
            )
        except:
            log("ERROR", "Unable to convert files to PDF")
            exit()
        
        log("INFO", "Converted Doujin to PDF")

        if self.params['clean'] == True:
            try:
                shutil.rmtree(self.dl_dir + f"\\{doujin['id']} - {doujin['title']}")
            except:
                log("WARN", "Unable to remove download directory")

    def verify_url(self, url):
        if SITE.lower() not in url:
            log("ERROR", "Given URL is invalid")
            exit()

    def download(self, url):
        log("INFO", "Starting session...")

        self.verify_url(url)

        self.inject_to_session()

        self.dl_dir = init_download_dir(SITE)
        
        doujin = self.parse_doujin(url)
        images = []

        log("INFO", "Downloading doujin")

        for current_page in range(1, doujin['pages'] + 1):
            page_url = f"{url}{current_page}"   

            page_image_url = self.get_page_image_url(page_url)
            self.download_content(doujin, current_page, page_image_url, images)

        self.convert_to_pdf(doujin, images)
        log("INFO", "Session concluded. Check for your download!")
        exit()

