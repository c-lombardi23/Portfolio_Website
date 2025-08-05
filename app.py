from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/projects")
def projects():
    return 'Project Page'

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/focal")
def focal():
    return render_template('focal.html')

@app.route("/portfolio")
def portfolio():
    return render_template('portfolio.html')

if __name__ == "__main__":

    app.run(debug=True)