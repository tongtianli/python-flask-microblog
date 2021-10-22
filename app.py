from flask import Flask, render_template, request
from jinja2 import Template
import datetime
from pymongo import MongoClient

def create_app():
    app = Flask(__name__)
    app.db = MongoClient(
        "mongodb+srv://user:KeOqF3YehmH2HAaa@micro-blog.sfnsg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    ).blogDB


    @app.route("/", methods=['GET', 'POST'])
    def home():
        if request.method == 'POST':
            entry_content = request.form.get('content')
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert({"content": entry_content, "date": formatted_date})

        entries_with_date = [
            (
                entry['content'],
                entry['date'],
                datetime.datetime.strptime(entry['date'], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]
        return render_template("home.html", entries=entries_with_date)

    return app