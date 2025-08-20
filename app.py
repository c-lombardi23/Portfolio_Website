from flask import Flask, render_template, request, flash, redirect, url_for, Response, send_file
from flask_mail import Mail, Message
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from dotenv import load_dotenv
import os
import time

from models import db, Article
from prometheus_setup import (
    VISITS,
    MESSAGES,
    RESUME_CLICKS,
    PORTFOLIO_VISITS,
    ABOUT_VISITS,
    RESUME_VISITS,
    BLOG_VISITS,
    EXTERNAL_CLICKS,
    HTTP_RESPONSES,
    REQUEST_LATENCY
)

load_dotenv()

app = Flask(__name__)

app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT"))
app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS") == 'True'
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['MAIL_DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")

mail = Mail(app)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.context_processor
def inject_request():
    return dict(request=request)

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        msg = Message(
            subject=f"New contact from {name}",
            sender=os.getenv("MAIL_USERNAME"),      
            recipients=[os.getenv("MAIL_USERNAME")],  
            body=f"From: {name} <{email}>\n\n{message}",
            reply_to=email  
        )
        try:
            mail.send(msg)
            flash("Message sent successfully!", "success")
            MESSAGES.inc() # increment total messages on prometheus
        except Exception as e:
            print(e)
            flash("Error sending message. Try again later.", "danger")
        return redirect(url_for("index"))

    return render_template("index.html")

@app.route("/admin")
def admin():
    articles = Article.query.order_by(Article.id.desc()).all()
    return render_template("admin.html", articles=articles)

@app.route("/delete_article/<int:article_id>")
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for("admin"))

@app.route("/blog")
def blog():
    BLOG_VISITS.inc()
    articles = Article.query.all()
    return render_template("blog.html", articles=articles)

@app.route("/article/<int:article_id>")
def view_article(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template("article.html", article=article)

@app.route("/")
def index():
    VISITS.inc() # increment total visits on prometheus
    return render_template('index.html')

@app.route("/about")
def about():
    ABOUT_VISITS.inc()
    return render_template('about.html')

@app.route("/portfolio")
def portfolio():
    PORTFOLIO_VISITS.inc()
    return render_template('portfolio.html')

@app.route("/resume")
def resume():
    RESUME_VISITS.inc()
    return render_template("resume.html")

@app.route("/download_resume")
def download_resume():
    RESUME_CLICKS.inc()
    return send_file("static/lombardi_resume_updated.pdf", as_attachment=True)

@app.route("/track/external_click", methods=["POST"])
def track_external_click():
    data = request.get_json()
    url = data.get("url")
    if url:
        EXTERNAL_CLICKS.labels(link=url).inc()
    return Response(status=204)

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.after_request
def track_http_response(response):
    HTTP_RESPONSES.labels(method=request.method, status=str(response.status_code)).inc()
    latency = time.time() - request.start_time
    REQUEST_LATENCY.labels(method=request.method, endpoint=request.path).observe(latency)
    return response


@app.route("/sitemap.xml", methods=["GET"])
def sitemap():
    pages = []

    # Static pages
    pages.append(url_for("index", _external=True))
    pages.append(url_for("about", _external=True))
    pages.append(url_for("resume", _external=True))
    pages.append(url_for("portfolio", _external=True))
    pages.append(url_for("projects", _external=True))
    pages.append(url_for("blog", _external=True))

    for article in Article.query.all():
        pages.append(url_for("view_article", article_id=article.id, _external=True))

    sitemap_xml = render_template("sitemap_template.xml", pages=pages)
    return Response(sitemap_xml, mimetype="application/xml")

if __name__ == "__main__":

    app.run(debug=True)