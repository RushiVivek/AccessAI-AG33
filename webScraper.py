import requests
from bs4 import BeautifulSoup
from PIL import Image
from urllib.parse import urljoin
from gemini import getAlt

class Scraper:
    def __init__(self):
        self.url = ""
        pass

    def scrape_url(self, url):

        issues = []

        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        self.url = req.url

        issues.extend(self.get_imgs(soup))
        return issues
    
    def get_imgs(self, soup):
        issue = []

        for img in soup.find_all('img'):
            if not img.get('alt'):
                img_src = img.get('src')

                if img_src:

                    if img_src[0:7] != "http://" and img_src[0:8] != "https://":
                        img_src = urljoin(self.url, img_src)

                    #get alt text here
                    imgAlt = getAlt(img_src)

                    issue.append(
                        {
                            'type': 'altMissing',
                            'suggestion': imgAlt,
                            'fix': f'<img src = "{str(img_src)}" alt = "{imgAlt}">',
                            'element': str(img), 
                        } 
                    )

        return issue
            

if __name__ == "__main__":
    sracpi = Scraper()
    changes = sracpi.scrape_url('http://192.168.106.164:5000/')

    if changes:
        print(changes)



