import os
import tempfile
from app import db, app
from models import Article

def get_content():

    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
        temp_name = tmp.name

    os.system(f'notepad "{temp_name}"')

    with open(temp_name, "r") as f:
        content = f.read()

    os.remove(temp_name)

    return content.strip()

with app.app_context():
    title = input("Enter title for article: ")
    print("Opening notepad...")
    content = get_content()

    if not content:
        print("No content entered...exiting")
    else:
        new_article = Article(
            title=title,
            content=content,
        )
    db.session.add(new_article)
    db.session.commit()
    print("Article added to database")