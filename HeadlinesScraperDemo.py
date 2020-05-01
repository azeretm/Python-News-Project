import requests
from time import sleep
from bs4 import BeautifulSoup



def getSoup(link):
    sleep(1)
    r = requests.get(link)
    return BeautifulSoup(r.text,'lxml')



def testIDNES():   
    base_url = "https://www.idnes.cz/zpravy/domaci/"
    
    headlines = []
    for i in range(1,6):
        
        soup = getSoup(base_url + str(i))
        
        for h in soup.find(id="list-art-count").findAll('h3'):
            headlines.append(h.text.strip())
            
    return headlines



def testAktualne():  
    base_url = "https://zpravy.aktualne.cz/domaci/?offset="
    
    headlines = []
    for i in range(5):
        
        soup = getSoup(base_url + str(i * 20))
        
        for h in soup.findAll("div", {"class": "left-column"})[0].findAll('h3'):
            headlines.append(''.join(h.find_all(text=True, recursive=False)).strip())
            
    return headlines
  

      

if __name__ == "__main__":
    headlines = testIDNES()
    
    print("Example of iDnes headlines: ")
    for h in headlines:
        print(f"- ", h)
       
    print("\n\n")
    
    headlines = testAktualne()
    print("Example of Aktuálně headlines: ")
    for h in headlines:
        print(f"- ", h)