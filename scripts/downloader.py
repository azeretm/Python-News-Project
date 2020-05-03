# Downloader
import requests
import pandas as pd
from time import sleep
from datetime import datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from tqdm import tqdm


class Downloader:
    '''
        Downlaods headlines.
    '''

    def __init__(self, url, dest_folder, verbose):

        self.url, self.url_path, self.url_base = self.splitUrl(url)
        self.dest_folder = dest_folder

        self.verbose = verbose

        self.articles = []
        self.articles_df = None

        if self.verbose:
            print("Succesfully initialized Downloader.")

    def splitUrl(self, url):
        '''
            ...
        '''

        url = urlparse(url)

        url_path = url.path + "?" + url.query
        url_base = url.scheme + "://" + url.netloc
        checked_url = url_base + url_path

        return checked_url, url_base, url_path

    def getSoup(self, link):
        '''
        '''

        sleep(1)
        r = requests.get(link)

        return BeautifulSoup(r.text, "lxml")

    def parseArticle(self, item):
        '''
        '''
        raise Exception("Method for parsing article is not implemented.")

    def downloadHeadlines(self, limit="01-01-2019"):
        '''
        '''
        raise Exception("method for downloading headlines is not implmented.")

    def saveToPandas(self):
        '''
        '''
        df = pd.DataFrame(self.articles, columns=["article_id", "slug", "date", "time", "is_updated", "headline", "excerpt", "article_url", "image_url", "scraped_at"])

        return df

    def saveToCsv(self):
        '''
        '''
        file_name = "articles_aktualne.cz__saved_" + datetime.now().strftime("%Y-%m-%d") + ".csv"

        self.articles_df.to_csv("../" + self.dest_folder + file_name, index=False)


class DownloaderAktualne(Downloader):
    '''
    '''

    def __init__(self, url, dest_folder, verbose=False):

        super().__init__(url, dest_folder, verbose)

    def parseArticle(self, item):
        '''
        '''

        link = item.findAll("a")[0]["href"]
        article_id = link.split("/")[3]
        slug = link.split("/")[2]

        time_label = item.findAll("div", {"class": "timeline__label"})[0]
        date = ''.join(time_label.find_all(text=True, recursive=False)).strip()
        time = date

        is_updated = False
        if time_label.find("span") is not None:
            is_updated = True

        headline = ''.join(item.find("h3").find_all(text=True, recursive=False)).strip()

        excerpt = item.findAll("div", {"class": "small-box__desc"})[0].text.strip()

        image_url = "https:" + item.find("img")["src"]

        article = {
            "article_id": article_id,
            "slug": slug,
            "date": date,
            "time": time,
            "is_updated": is_updated,
            "headline": headline,
            "excerpt": excerpt,
            "article_url": link,
            "image_url": image_url,
            "scraped_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }

        self.articles.append(article)

    def downloadHeadlines(self):
        '''
        '''

        for i in range(1):

            posts_url = self.url + "?offset=" + str(i * 20)
            soup = self.getSoup(posts_url)

            posts = soup.findAll("div", {"class": "timeline"})[0].findAll("div", {"class": "small-box"})

            for post in posts:
                self.parseArticle(post)

        self.articles_df = self.saveToPandas()


class DownloaderIdnes(Downloader):
    '''
    '''

    def __init__(self, url, dest_folder, verbose=False):

        super().__init__(url, dest_folder, verbose)

    def parseArticle(self):
        '''
        '''
        pass

    def downloadHeadlines(self):
        '''
        '''
        pass


#d = DownloaderAktualne("https://zpravy.aktualne.cz/domaci/", dest_folder="data/", verbose=True)
# d.downloadHeadlines()
# d.saveToCsv()
# print(d.articles)
