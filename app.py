from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

from models import db, Article

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

    if Article.query.count() == 0:
        sample_articles = [
            Article(title="Welcome to Flask", content="This is your first article!"),
            Article(title="SQLAlchemy is great", content="You can easily manage your database with SQLAlchemy."),
            Article(title="SQLite Example", content="SQLite is perfect for small projects and prototyping.")
        ]
        db.session.bulk_save_objects(sample_articles)
        db.session.commit()

@app.context_processor
def inject_request():
    return dict(request=request)

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
        except Exception as e:
            print(e)
            flash("Error sending message. Try again later.", "danger")
        return redirect(url_for("index"))

    return render_template("index.html")

@app.route("/blog")
def blog():
    articles = Article.query.all()
    return render_template("blog.html", articles=articles)

@app.route("/article/<int:article_id>")
def view_article(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template("article.html", article=article)

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

@app.route("/resume")
def resume():
    return render_template("resume.html")

if __name__ == "__main__":

    app.run(debug=True)