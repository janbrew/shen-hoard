# shen-hoard

Shenanigan hoarding. Scraping random content from image boards and stuff

## Requirements
- python
- beautifulsoup4
- requests
- Pillow
- dotenv
- click

## Usage

    py scraper.py {command} {args}

### Commands
- danbooru
- gelbooru
- safebooru
- nhentai
- zerochan
- yandere

### Arguments

###### *Short names are not available (Can't think of aliases)*

|   Options   |  Values | Description |
| :--------:  | :-----: | :---------: |
| --url       | None    | The website section/page to scrape. For `nhentai`, the specific doujinshi url |
| --pages     | 1~      | The amount of pages to scrape. Depends on what the website can load
| --score     | 0~      | The minimum score of a post to be scraped
| --rating    | q e s g | `q` Questionable `e` Explicit    `s` Sensitive/Safe `g` General 
| --scope     | img, vid | `img` Only Image `vid` With Video
| --clearance | None    | initially required cookie from nhentai that validates request
| --token     | None    | initially required cookie from nhentai that validates request
| --save      | flagged | Flag for saving cookies for future use
| --clean     | flagged | Flag for removing doujinshi subdirectory
| --zhash     | None    | initially required cookie from zerochan that lets access to `Subscribed` section for registered users
| --zid       | None    | initially required cookie from zerochan that lets access to `Subscribed` section for registered users

#### Argument Long Descriptions

`url` - The URL website to scrape. Users are the ones to browse to their preferred page/section to scrape

`pages` - The amount of pages to scrape. By default, it starts with the page provided by the url which is `1`. Users can start at a specific page by navigating to that page and using the URL of that page.

`score` - The minimum upvote/score/favorite a post must have to be included in the scraping process. Otherwise, it will be skipped.

`rating` - Categories or types that posts must have to be scraped. `q e s g` are all available for danbooru and gelbooru `e s g` are available for safebooru and yandere and `s` is Safe

`scope` - Content types to include in the process. 

`zhash` and `zid` - Cookies that lets the scraper access the **Subscribed** section (Registered user feature)

`clearance` and `token` - Cookies that validate request for the website

`save` - Configure environment variables to save the just-inputted cookies for future use.

`clean` - Remove the subdirectory where doujinshi pages were downloaded after session

### Examples 
#### 1. danbooru

##### Usage
    py scraper.py danbooru --url https://mybooruurl --pages 3 --score 10 --rating q e s --scope vid 


#### 2. gelbooru

##### Usage
    py scraper.py gelbooru --url https://mybooruurl --pages 3 --score 10 --rating q e s --scope vid 

#### 3. safebooru

##### Usage
    py scraper.py safebooru --url https://mybooruurl --pages 3 --score 10 --rating e s

#### 4. yandere

##### Usage
    py scraper.py yandere --url https://mybooruurl --pages 3 --score 10 --rating q e s --scope vid 

#### 5. nhentai

##### Usage

###### Deleting the Mess After Download
    py scraper.py nhentai https://nhentai.net/g/123456 --clearance cookie1 --token cookie 2 --save --clean

###### Keeping the Mess After Download
    py scraper.py nhentai https://nhentai.net/g/123456 --clearance cookie1 --token cookie 2 --save

##### Steps in getting the cookies
i. Open nhentai.net and authenticate yourself (captcha)

ii. Open the developer tools / inspect 
> Ctrl + Shift + I / F12

iii. Go to `Storage` section and copy the value of the two cookies
> For chromium browsers, the `Storage` section may be accessed through the >> icon at the far right part of the devtools

> [!IMPORTANT]
> Cookies expire after a year I think. Just in case you're still using this junk and whether if it still works till that time

#### 6. zerochan

Although this can scrape the Subscribed section, it does not allow for scraping registered user-only contents (Will find a way soon)

##### Usage
    py scraper.py zerochan --url https://zerochanurl --zhash cookie1 --zid cookie2 --pages 10 --score 5 --keep

##### Steps in getting the cookies
i. Open nhentai.net and authenticate yourself (captcha)

ii. Open the developer tools / inspect 
> Ctrl + Shift + I / F12

iii. Go to `Storage` section and copy the value of the two cookies
> For chromium browsers, the `Storage` section may be accessed through the >> icon at the far right part of the devtools

> [!IMPORTANT]
> The cookies expire after a month. Make sure to change it when the time comes if ever you're still using this junk or this still works

## Supported Sites
- #### [danbooru](https://danbooru.donmai.us/)
- ####  [gelbooru](https://gelbooru.com/index.php)
- #### [safebooru](https://safebooru.org)
- #### [nhentai.net](https://nhentai.net)
- #### [yande.re](https://yande.re)
- #### [zerochan](https://www.zerochan.net/)