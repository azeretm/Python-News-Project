# Downloader
import requests
from time import sleep
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from tqdm import tqdm



class Downloader:
    '''
        Downlaods headlines.
    '''
    
    def __init__(self, url, verbose=False):
        
        
        self.url, self.url_path, self.url_base = self.splitUrl(url)
        
        self.verbose = verbose
        
        
        self.headlines = []
        
        
        if self.verbose:
            print("Succesfully initialized Downloader.")
        
    
    def splitUrl(self, url):
        '''
            ...
        '''
        
        url = urlparse(url)
        
        url_path = url.path + "?" + url.query
        url_base = url.scheme + "://" + url.netloc
        
        return (url_base + url_path), url_base, url_path
    
    
    def getSoup(self, link):
        ''' 
        '''
        
        sleep(1)
        r = requests.get(link)
        
        return BeautifulSoup(r.text, 'lxml')
    
    
    def downloadHeadlines(self, limit="01-01-2019"):
        
        for i in range(5):
            
            posts_url = self.url + "?offset=" + str(i * 20)
            soup = self.getSoup(posts_url)
            
            for h in soup.findAll("div", {"class": "left-column"})[0].findAll('h3'):
                self.headlines.append(''.join(h.find_all(text=True, recursive=False)).strip())

        
    
    


d = Downloader("https://zpravy.aktualne.cz/domaci/")
d.downloadHeadlines()
print(d.headlines)

