import click
import os
from src.main.scraper import *

BOORU_HELP = {
    "url" : "The website url to scrape",
    "pages" : "The amount of pages to scrape. Defaults to 1",
    "score" : "The minimum score of posts to scrape. Defaults to 0",
    "rating" : {
        "booru" : "The rating of posts to scrape. Defaults to all. OPTIONS: q [QUESTIONABLE] e [EXPLICIT] s [SENSITIVE] g [GENERAL]",
        "yandere" : "The rating of posts to scrape. Defaults to all. OPTIONS: q [QUESTIONABLE] e [EXPLICIT] s [SAFE]"
    },
    "scope" : {
        "danbooru" : "The content type scope of posts to scrape. Defaults to vid. OPTIONS: img [IMAGE-ONLY] vid [CONTAIN VIDEO]",
        "gelbooru" : "The content type scope of posts to scrape. Defaults to vid. OPTIONS: img [IMAGE-ONLY] vid [CONTAIN VIDEO]",
        "safebooru" : "The content type scope of posts to scrape. Defaults to gif. OPTIONS: img [IMAGE-ONLY] gif [CONTAIN GIF]"
    }
}

NHENTAI_HELP = {
    "url" : "The website url to scrape",
    "clearance" : "The cf_clearance cookie of your site. Defaults to your set cookie [NONE IF FIRST USE]",
    "token" : "The csrftoken of your site. Defaults to your set cookie [NONE IF FIRST USE]",
    "save" : "Toggleable to save cookies for future use. Do not pass to set to False",
    "clean" : "Toggleable to remove download directory. Do not pass to set to False"
}

ZEROCHAN_HELP = {
    "url" : "The website url to scrape",
    "pages" : "The amount of pages to scrape",
    "score" : "The minimum score of post to scrape",
    "zhash" : "z_hash cookie for accessing 'Subscribed'. Requires user log in and retrieve cookie. Defaults to your set cookie [NONE IF FIRST USE]",
    "zid" : "z_id cookie for accessing 'Subscribed'. Requires user log in and retrieve cookie. Defaults to your set cookie [NONE IF FIRST USE]",
    "save" : "Toggleable to save input cookies for future use. Do not pass to set to False"
}

@click.group("scraper")
def scraper():
    """
    Commands for available sites to scrape
    """
    pass

@click.command("danbooru")
@click.option("--url", help =  BOORU_HELP['url'], type = str, required = True)
@click.option("--pages", help = BOORU_HELP['pages'], type = int, default = 1)
@click.option("--score", help = BOORU_HELP['score'], type = int, default = 0)
@click.option("--rating", help = BOORU_HELP['rating']['booru'], type = str, default = "all")
@click.option("--scope", help = BOORU_HELP['scope']['danbooru'], type = str, default = "vid")
def danbooru(url, pages, score, rating, scope):
    dl = DanbooruDownloader(
        pages = pages, 
        min_score = score, 
        ratings = rrating.split(" ") if " " in rating else "q e s g".split(" ") if rating == "all" else [rating], 
        scope = scope
        )

    dl.download(url)

@click.command("gelbooru")
@click.option("--url", help =  BOORU_HELP['url'], type = str, required = True)
@click.option("--pages", help = BOORU_HELP['pages'], type = int, default = 1)
@click.option("--score", help = BOORU_HELP['score'], type = int, default = 0)
@click.option("--rating", help = BOORU_HELP['rating']['booru'], type = str, default = "all")
@click.option("--scope", help = BOORU_HELP['scope']['gelbooru'], type = str, default = "vid")
def gelbooru(url, pages, score, rating, scope):
    dl = GelbooruDownloader(
        pages = pages, 
        min_score = score, 
        ratings = rating.split(" ") if " " in rating else "q e s g".split(" ") if rating == "all" else [rating], 
        )

    dl.download(url)

@click.command("safebooru")
@click.option("--url", help =  BOORU_HELP['url'], type = str, required = True)
@click.option("--pages", help = BOORU_HELP['pages'], type = int, default = 1)
@click.option("--score", help = BOORU_HELP['score'], type = int, default = 0)
@click.option("--rating", help = BOORU_HELP['rating']['booru'], type = str, default = "all")
def safebooru(url, pages, score, rating, scope):
    dl = SafebooruDownloader(
        pages = pages, 
        min_score = score, 
        ratings = rating.split(" ") if " " in rating else "e s g".split(" ") if rating == "all" else [rating]
        )

    dl.download(url)

@click.command("yandere")
@click.option("--url", help =  BOORU_HELP['url'], type = str, required = True)
@click.option("--pages", help = BOORU_HELP['pages'], type = int, default = 1)
@click.option("--score", help = BOORU_HELP['score'], type = int, default = 0)
@click.option("--rating", help = BOORU_HELP['rating']['yandere'], type = str, default = "all")
def safebooru(url, pages, score, rating):
    dl = YandereDownloader(
        pages = pages, 
        min_score = score, 
        ratings = rating.split(" ") if " " in rating else "q e s".split(" ") if rating == "all" else [rating]
        )

    dl.download(url)

@click.command("nhentai")
@click.option("--url", help = NHENTAI_HELP['url'], type = str, required = True)
@click.option("--clearance", help = NHENTAI_HELP['clearance'], type = str, default = "")
@click.option("--token", help = NHENTAI_HELP['token'], type = str, default = "")
@click.option("--save", help = NHENTAI_HELP['save'], is_flag = True)
@click.option("--clean", help = NHENTAI_HELP['clean'], is_flag = True)
def nhentai(url, clearance, token, save, clean):
    dl = nHentaiDownloader(
        clearance = clearance, 
        token = token, 
        save = save, 
        clean = clean
        )

    dl.download(url)

@click.command("zerochan")
@click.option("--url", help = ZEROCHAN_HELP['url'], type = str, required = True)
@click.option("--pages", help = ZEROCHAN_HELP['pages'], type = int, default = 1)
@click.option("--score", help = ZEROCHAN_HELP['score'], type = int, default = 0)
@click.option("--zhash", help = ZEROCHAN_HELP['zhash'], type = str, default = "")
@click.option("--zid", help = ZEROCHAN_HELP['zid'], type = str, default = "")
@click.option("--save", help = ZEROCHAN_HELP['save'], is_flag = True)
def zerochan(url, pages, score, zhash, zid, save):
    dl = ZerochanDownloader(
        pages = pages,
        min_score = score,
        z_hash = zhash,
        z_id = zid,
        save = save
    )

    dl.download(url)

scraper.add_command(danbooru)
scraper.add_command(gelbooru)
scraper.add_command(safebooru)
scraper.add_command(nhentai)
scraper.add_command(zerochan)

if __name__ == "__main__":
    scraper()
