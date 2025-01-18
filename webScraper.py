import requests
from bs4 import BeautifulSoup
from PIL import Image
from urllib.parse import urljoin
from gemini import getAlt, getLabel

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
                    
                    simg = str(img)
                    if "alt" in simg:
                        simg = simg.split("alt")
                        simg[1] = simg[1].split("=")[1]
                        i = 0
                        while simg[1][i] == " ":
                            i += 1
                        simg[1] = simg[1].split(simg[1][i])[2]
                        simg = simg[0] + simg[1]

                    issue.append(
                        {
                            'type': 'altMissing',
                            'suggestion': imgAlt,
                            'fix': f'{simg[:-2]} alt = "{imgAlt}"/>',
                            'element': str(img), 
                        } 
                    )

        return issue
            
    def get_label(self, soup):
        issue = []

        for inp in soup.find_all('input, textarea'):

            if not inp.get('id'):
                continue
            
            print(inp)

            label = soup.find('label', attrs={'for': inp['id']})
            gemLabel = getLabel(inp, label)
            if gemLabel == 'y':
                continue
            
            issue.append({
                'type': 'labelChanged',
                'suggestion': gemLabel,
                'fix': f'<label for="{inp["id"]}">{gemLabel}</label>',
                'element': str(inp), 
            })

        return issue


if __name__ == "__main__":
    sracpi = Scraper()
    changes = sracpi.scrape_url('http://192.168.106.164:5000/')

    if changes:
        print(changes)



