from flask import Flask, render_template, request
from webScraper import Scraper
from urllib.parse import urljoin
from bs4 import BeautifulSoup

app = Flask(__name__, template_folder="templates")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("website_link")
        analyzer = Scraper()
        base, soup, issues = analyzer.scrape_url(url)

        # print(issues)

        # for issue in issues:
        #     if issue['type'] == 'altMissing':
        #         html.replace(issue['element'], issue['fix'])
        #         print(issue['fix'], issue['element'])
            
        #     if issue['type'] == 'labelMissing':
        #         if issue['element']:
        #             html.replace(issue['element'], issue['fix'])
        #         else:
        #             html.replace(issue['input'], f"{issue['input']} {issue['fix']}")
        

        # soup = BeautifulSoup(html, 'html.parser')
        
        for atag in soup.find_all('a'):
            if 'href' in atag.attrs:
                atag['href'] = urljoin(base, atag['href'])
        
        for img in soup.find_all('img'):
            if 'src' in img.attrs:
                img['src'] = urljoin(base, img['src'])
        
        for link in soup.find_all('link'):
            if 'href' in link.attrs:
                link['href'] = urljoin(base, link['href'])
        
        for script in soup.find_all('script'):
            if 'src' in script.attrs:
                script['src'] = urljoin(base, script['src'])
        
        html = str(soup)

        return render_template("index.html", output=html)

    return render_template("index.html")

if __name__ == "__main__":
	app.run(debug=True)