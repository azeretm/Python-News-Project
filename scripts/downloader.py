# Downloader
import os
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
    
    def __init__(self, url, save_to, verbose):
        
        
        self.url, self.url_path, self.url_base = self.splitUrl(url)
        self.save_to = save_to
        
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
        
        url_path = url.path
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
  
              
    
    def saveToPandas(self, data):
        '''
        '''
        df = pd.DataFrame(data, columns=["article_id", "slug", "date", "time", "is_updated", "headline", "excerpt", "article_url", "scraped_at"])
        
        return df
    
   
    
    def saveToCsv(self, data):
        '''
        '''
        file_path = "../" + self.save_to
        
        if os.path.exists(file_path):
            # Saves new rows to existing file
            df = pd.read_csv(file_path, sep=",")
        
            df_diff = pd.concat([df, data], ignore_index=True)
            df_diff = df_diff.drop_duplicates(subset="article_id", keep="last")
            df_diff.to_csv(file_path, index=False)
        
        else:
            # Saves to new file
            data.to_csv(file_path, index=False)



class DownloaderAktualne(Downloader):
    '''
    '''
    
    def __init__(self, url, save_to, verbose=False):
        
        super().__init__(url, save_to, verbose)
     
        
    
    def parseArticle(self, item):
        '''
        '''

        # Finds article_url, gets article ID and Slug from the link
        link = item.findAll("a")[0]["href"]
        slug = link.split("/")[2]
        article_id = link.split("/")[3]
        article_url = self.url_base + link
        
        # Finds date and time when the article was published
        time_label = item.findAll("div", {"class": "timeline__label"})[0]
        date = ''.join(time_label.find_all(text=True, recursive=False)).strip()
        time = date
        
        # Checks whether the article was updated ("aktualizováno")
        is_updated = False
        if time_label.find("span") is not None:
            is_updated = True
        
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
    
    def __init__(self, url, save_to, verbose=False):
        
        super().__init__(url, save_to, verbose)    
       
        
    
    def parseArticle(self, item):
        '''
        '''

        # Finds article_url, gets article ID and Slug from the link
        link = item.findAll("a", {"class":"art-link"})[0]["href"]
        slug = link.split(".")[2].split("/")[-1]
        article_id = link.split(".")[-1]
        article_url = link
        
        # Finds date and time when the article was published
        time_label = item.findAll("span", {"class": "time"})
        is_updated = False
        
        if time_label != []:
            date = time_label[0]["datetime"]
            time = date
            
            # Checks whether the article was updated ("aktualizováno")
            if time_label[0].find("span") is not None:
                is_updated = True
        else:
            date = None
            time = None
        
            
        # Gets the article headline
        headline = item.find("h3").text.strip()
        
        # Gets the article excerpt
        excerpt = item.findAll("p", {"class": "perex"})[0].text.strip()

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
    
    
    
    def downloadHeadlines(self):
        '''
        '''
        
        for i in range(1,4):
        
            posts_url = self.url + str(i)
            soup = self.getSoup(posts_url)
            
            posts = soup.find(id="list-art-count").findAll("div", {"class": "art"})
            
            for post in posts:
                self.parseArticle(post)
        
        
        self.articles_df = self.saveToPandas(self.articles)
    
    


#d = DownloaderAktualne("https://zpravy.aktualne.cz/domaci/", dest_folder="data/", verbose=True)
#d.downloadHeadlines()
#d.saveToCsv()
#print(d.articles)
        
    

#d = DownloaderIdnes("https://www.idnes.cz/zpravy/domaci/", save_to="data/articles_iDnes.cz.csv", verbose=True)
#d.downloadHeadlines()
#a=d.articles_df
#d.saveToCsv(d.articles_df)



