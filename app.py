from flask import Flask, render_template, request
from webScraper import Scraper

app = Flask(__name__, template_folder="templates")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("website_link")
        analyzer = Scraper()
        html, issues = analyzer.scrape_url(url)

        # print(issues)

        for issue in issues:
            if issue['type'] == 'altMissing':
                html.replace(issue['element'], issue['fix'])
            
            if issue['type'] == 'labelMissing':
                if issue['element']:
                    html.replace(issue['element'], issue['fix'])
                else:
                    html.replace(issue['input'], f"{issue['input']} {issue['fix']}")
                

        return render_template("index.html", output=html)

    return render_template("index.html")

if __name__ == "__main__":
	app.run(debug=True)