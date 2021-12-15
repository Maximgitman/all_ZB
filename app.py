from cs50 import SQL
from flask import Flask, render_template, request

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///static/emotions.db")


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    # Show last 3 results from DataBase
    results = db.execute("SELECT * FROM emotions ORDER BY id DESC LIMIT 3")
    return render_template("index.html", results=results)


@app.route("/emotion", methods=["GET", "POST"])
def emotions():
    if request.method == "POST":
        # Show last 3 results from DataBase
        results = db.execute("SELECT * FROM emotions ORDER BY id DESC LIMIT 3")
        return render_template("emotion.html", results=results)
    else:
        results = db.execute("SELECT * FROM emotions ORDER BY id DESC LIMIT 3")
        return render_template("emotion.html", results=results)


@app.route("/text-from-image", methods=["GET", "POST"])
def txt_from_img():
    if request.method == "POST":
        # Show last 3 results from DataBase
        results = db.execute("SELECT * FROM emotions ORDER BY id DESC LIMIT 3")
        return render_template("text-from-image.html", results=results)
    else:
        results = db.execute("SELECT * FROM emotions ORDER BY id DESC LIMIT 3")
        return render_template("text-from-image.html", results=results)


@app.route("/similar-text", methods=["GET", "POST"])
def similar_txt():
    if request.method == "POST":
        # Show last 3 results from DataBase
        results = db.execute("SELECT * FROM emotions ORDER BY id DESC LIMIT 3")
        return render_template("similar-text.html", results=results)
    else:
        results = db.execute("SELECT * FROM emotions ORDER BY id DESC LIMIT 3")
        return render_template("similar-text.html", results=results)