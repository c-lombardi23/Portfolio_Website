from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

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

mail = Mail(app)

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