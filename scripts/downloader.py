# Downloader
import os
import requests
import pandas as pd
import re
from time import sleep
from datetime import datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from tqdm import tqdm


class Downloader:
    '''
        Main class for Downloader, all the necessary methods are outlined here.
    '''

    def __init__(self, url, save_to, verbose):

        self.url, self.url_base, self.url_path = self.splitUrl(url)
        self.save_to = save_to

        self.verbose = verbose

        self.articles = []
        self.articles_df = None


    def splitUrl(self, url):
        '''
            Checks the URL and splits it into base and path parts.
        '''

        url = urlparse(url)

        url_path = url.path
        url_base = url.scheme + "://" + url.netloc
        checked_url = url_base + url_path

        return checked_url, url_base, url_path


    def getSoup(self, link):
        '''
            Downloads the page and creates BeautifulSoup.
        '''

        sleep(1) # From Aktualne.cz robots.txt
        r = requests.get(link)

        return BeautifulSoup(r.text, "lxml")


    def parseArticle(self, item):
        '''
            Implemented in child class.
        '''
        raise Exception("Method for parsing article is not implemented.")


    def downloadHeadlines(self, limit="01-01-2019"):
        '''
            Implemented in child class.
        '''
        raise Exception("Method for downloading headlines is not implmented.")


    def saveToPandas(self, data):
        '''
            Saves the articles objects into pd.DataFrame.
        '''
        df = pd.DataFrame(data, columns=["article_id", "slug", "date", "time", "is_updated", "headline", "excerpt", "article_url", "scraped_at"])

        return df


    def saveToCsv(self):
        '''
            Saves the DataFrame to CSV.
        '''
        data = self.articles_df
        file_path = self.save_to

        if os.path.exists(file_path):
            # Saves new rows to existing file
            df = pd.read_csv(file_path, sep=",")

            # Order of the data is important for updating the article date since we keep the last record
            df_diff = pd.concat([df, data], ignore_index=True)
            df_diff = df_diff.drop_duplicates(subset="article_id", keep="last")
            df_diff.to_csv(file_path, index=False)

        else:
            # Saves to new file
            data.to_csv(file_path, index=False)



class DownloaderAktualne(Downloader):
    '''
        Downloader for Aktualne.cz.
    '''

    def __init__(self, url, save_to, verbose=False):

        super().__init__(url, save_to, verbose)

        if self.verbose:
            print("Succesfully initialized DownloaderAktualne.")


    def getDate(self, item):
        '''
            Parses time, date and is_updated from html block.
        '''

        # Finds date and time when the article was published
        time_label = item.findAll("div", {"class": "timeline__label"})[0]
        str_raw_date = ''.join(time_label.find_all(text=True, recursive=False)).strip()

        if str_raw_date[0].isdigit() is True:
            raw_date = datetime.strptime(str_raw_date, '%d. %m. %Y %H:%M')
            date = raw_date.date()
            time = raw_date.time()
        else:
            date = None
            time = None

        # Checks whether the article was updated ("aktualizováno")
        is_updated = False
        if time_label.find("span") is not None:
            is_updated = True

        return is_updated, date, time


    def parseArticle(self, item):
        '''
            Parses article item and appends it to the list of articles.
        '''

        # Finds article_url, gets article ID and Slug from the link
        link = item.findAll("a")[0]["href"]
        article_id = link.rsplit("/", 2)[1]
        slug = link.rsplit("/", 2)[0].rsplit("/", 1)[1]
        article_url = self.url_base + link


        is_updated, date, time = self.getDate(item)

        # Gets the article headline
        headline = ''.join(item.find("h3").find_all(text=True, recursive=False)).strip()

        # Gets the article excerpt
        excerpt = item.findAll("div", {"class": "small-box__desc"})[0].text.strip()

        # Creates article object
        article = {
            "article_id": article_id,
            "slug": slug,
            "date": date,
            "time": time,
            "is_updated": is_updated,
            "headline": headline,
            "excerpt": excerpt,
            "article_url": article_url,
            "scraped_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }

        self.articles.append(article)


    def downloadHeadlines(self, from_page = 1, to_page = 5, bulk_size = 40):
        '''
            Downloads the requested pages with articles.
        '''

        if from_page > to_page and from_page <= 0:
            raise Exception("Defined range of articles is invalid (valid: to_page >= from_page > 0).")

        if bulk_size <= 0:
            raise Exception("Bulk size must be greater than 0.")


        count_bulks = 0

        for i in tqdm(range(from_page, to_page+1)):

            posts_url = self.url + "?offset=" + str((i-1) * 20)
            soup = self.getSoup(posts_url)

            posts = soup.findAll("div", {"class": "timeline"})[0].findAll("div", {"class": "small-box"})

            for post in posts:
                self.parseArticle(post)


            if (i % bulk_size) == 0:
                count_bulks += 1
                sleep(2)

                if self.verbose:
                    print("%s. bulk of articles successfully downloaded." % count_bulks)


        self.articles_df = self.saveToPandas(self.articles)

        if self.verbose:
            print("Articles were successfully downloaded. Access DataFrame '.articles_df' or json list '.articles'.")



class DownloaderIdnes(Downloader):
    '''
        Downloader for iDnes.cz.
    '''

    def __init__(self, url, save_to, verbose=False):

        super().__init__(url, save_to, verbose)

        if self.verbose:
            print("Succesfully initialized DownloaderIdnes.")


    def getDate(self, item):
        '''
            Parses time, date and is_updated from html block.
        '''

        # Finds date and time when the article was published
        time_label = item.findAll("span", {"class": "time"})

        if time_label != []:
            date = re.findall('\d{4}\-\d{2}\-\d{2}', str(time_label))[0]
            time = re.findall('\d{2}\:\d{2}\:\d{2}', str(time_label))[0]
        else:
            date = None
            time = None

        # Checks whether the article was updated ("aktualizováno")
        is_updated = False
        if ("aktualizováno" in str(time_label)) is True:
            is_updated = True

        return is_updated, date, time


    def parseArticle(self, item):
        '''
            Parses article item and appends it to the list of articles.
        '''

        # Finds article_url, gets article ID and Slug from the link
        link = item.findAll("a", {"class": "art-link"})[0]["href"]
        slug = link.split(".")[2].split("/")[-1]
        article_id = link.split(".")[-1]
        article_id = article_id.split("/")[0]
        article_url = link

        is_updated, date, time = self.getDate(item)

        # Gets the article headline
        headline = item.find("h3").text.strip()

        # Gets the article excerpt
        excerpt = ''.join(item.find("p").find_all(text=True, recursive=False)).strip()

        # Creates article object
        article = {
            "article_id": article_id,
            "slug": slug,
            "date": date,
            "time": time,
            "is_updated": is_updated,
            "headline": headline,
            "excerpt": excerpt,
            "article_url": article_url,
            "scraped_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }

        # Rules out adding Advertisement placeholder to the dataset
        if link != "https://www.example.com":
            self.articles.append(article)


    def downloadHeadlines(self, from_page = 1, to_page = 5, bulk_size = 40):
        '''
            Downloads the requested pages with articles.
        '''

        if from_page > to_page:
            raise Exception("Defined range of articles is invalid (from_page > to_page).")

        if bulk_size <= 0:
            raise Exception("Bulk size must be greater than 0.")


        count_bulks = 0

        for i in tqdm(range(from_page, to_page+1)):

            posts_url = self.url + str(i)
            soup = self.getSoup(posts_url)

            posts = soup.find(id="list-art-count").findAll("div", {"class": "art"})

            for post in posts:
                self.parseArticle(post)


            if (i % bulk_size) == 0:
                count_bulks += 1
                sleep(2)

                if self.verbose:
                    print("%s. bulk of articles successfully downloaded." % count_bulks)


        self.articles_df = self.saveToPandas(self.articles)

        if self.verbose:
            print("Articles were successfully downloaded. Access DataFrame '.articles_df' or json list '.articles'.")

