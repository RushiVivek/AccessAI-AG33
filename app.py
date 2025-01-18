from flask import Flask, render_template, request
from webScraper import Scraper

app = Flask(__name__, template_folder="templates")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("website_link")
        analyzer = Scraper()
        issues = analyzer.scrape_url(url)

        print(issues)

        return render_template("index.html", issues=issues)

    return render_template("index.html")

if __name__ == "__main__":
	app.run(debug=True)