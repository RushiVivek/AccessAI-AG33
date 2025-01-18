from flask import Flask, render_template, request
from webAnalyzer import AccessibliltyAnalyzer

app = Flask(__name__, template_folder="templates")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
		url = request.form.get("website_link")
		analyzer = AccessibliltyAnalyzer()
        issues = analyzer.analyze_website(url)

		return render_template("index.html", issues=issues)

	return render_template("index.html")

if __name__ == "__main__":
	app.run(debug=True)