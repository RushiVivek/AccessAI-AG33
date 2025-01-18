import requests
from bs4 import BeautifulSoup
from PIL import Image
from urllib.parse import urljoin
from gemini import getAlt, getLabel

class Scraper:
    def __init__(self):
        self.url = ""
        self.html = ""
        self.soup = None

    def scrape_url(self, url):

        issues = []

        req = requests.get(url)
        self.soup = BeautifulSoup(req.text, 'html.parser')
        self.url = req.url
        self.html = req.text

        self.get_imgs()
        self.get_label()
        self.html = str(self.soup)
        return [self.url, self.soup, issues]
    
    def get_imgs(self):
        issue = []

        for img in self.soup.find_all('img'):
            if not img.get('alt') or img.get('alt') == '':
                img_src = img.get('src')

                if img_src:

                    if img_src[0:7] != "http://" and img_src[0:8] != "https://":
                        img_src = urljoin(self.url, img_src)

                    #get alt text here
                    imgAlt = getAlt(img_src)
                    
                    #removing empty alt
                    simg = str(img)
                    if "alt" in simg:
                        simg = simg.split("alt")
                        simg[1] = "=".join(simg[1].split("=")[1:])
                        i = 0
                        while simg[1][i] == " ":
                            i += 1
                        ch = simg[1][i]
                        simg[1] = ch.join(simg[1].split(ch)[2:])
                        simg = simg[0] + simg[1]

                    img['alt'] = imgAlt
                    # issue.append(
                    #     {
                    #         'type': 'altMissing',
                    #         'fix': f'{simg[:-2]} alt = "{imgAlt}"/>',
                    #         'element': str(img), 
                    #     } 
                    # )

        return issue
            
    def get_label(self):
        issue = []

        for inp in self.soup.find_all('input, textarea'):

            if not inp.get('id'):
                continue
            
            print(inp)

            label = self.soup.find('label', attrs={'for': inp['id']})
            gemLabel = getLabel(inp, label)
            if gemLabel == 'y':
                continue
            
            if not label:
                label = self.soup.new_tag('label')
                label['for'] = inp['id']
                label.string = gemLabel
                inp.insert_before(label)
            else:
                label.string = gemLabel
            # issue.append({
            #     'type': 'labelChanged',
            #     'fix': f'<label for="{inp["id"]}">{gemLabel}</label>',
            #     'element': str(label) if label else None,
            #     'input': str(inp),
            # })

        return issue


if __name__ == "__main__":
    sracpi = Scraper()
    changes = sracpi.scrape_url('http://192.168.106.164:5000/')

    if changes:
        print(changes)



