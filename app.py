from cs50 import SQL
from flask import Flask, render_template, request
from emotion_detection.sentiment import SemanticRu


Sentiment_ru = SemanticRu()

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///static/allzb.db")


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
    results = db.execute("SELECT * FROM emotion ORDER BY id DESC LIMIT 3")
    return render_template("index.html", results=results)


@app.route("/emotion", methods=["GET", "POST"])
def emotion():
    if request.method == "POST":
        # Getting input text into base
        text_input = request.form.get("text_input")
        if not text_input:  # If there is no name, showing erros page
            return render_template("error.html", message="Missing text, try again")

        predict = Sentiment_ru.inference(txt=text_input)

        # Save it into SQL
        db.execute("INSERT INTO emotion (input, output, score) VALUES(?, ?, ?)", text_input, predict[0], predict[1])

        # Show last 3 results from DataBase
        results = db.execute("SELECT * FROM emotion ORDER BY id DESC LIMIT 4")
        return render_template("emotion.html", results=results)

    else:
        # Show last 3 results from DataBase
        results = db.execute("SELECT * FROM emotion ORDER BY id DESC LIMIT 3")
        return render_template("emotion.html", results=results)


@app.route("/text-from-image", methods=["GET", "POST"])
def txt_from_img():
    if request.method == "POST":
        # Show last 3 results from DataBase
        results = db.execute("SELECT * FROM emotion ORDER BY id DESC LIMIT 3")
        return render_template("text-from-image.html", results=results)
    else:
        results = db.execute("SELECT * FROM emotion ORDER BY id DESC LIMIT 3")
        return render_template("text-from-image.html", results=results)


@app.route("/similar-text", methods=["GET", "POST"])
def similar_txt():
    if request.method == "POST":
        # Show last 3 results from DataBase
        results = db.execute("SELECT * FROM emotion ORDER BY id DESC LIMIT 3")
        return render_template("similar-text.html", results=results)
    else:
        results = db.execute("SELECT * FROM emotion ORDER BY id DESC LIMIT 3")
        return render_template("similar-text.html", results=results)