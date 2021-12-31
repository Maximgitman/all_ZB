from cs50 import SQL
from flask import Flask, flash, render_template, request, redirect
from emotion_detection.sentiment import SemanticRu
from werkzeug.utils import secure_filename
from text_recognition.text_recognition import ocr_text
from similar_recognition import similarity
import os
import gensim

model = gensim.models.KeyedVectors.load_word2vec_format('static/w2v.bin', binary=True)
index2word_set = set(model.index_to_key)

# Initialisation class for semantic ruBERT
Sentiment_ru = SemanticRu()

UPLOAD_FOLDER = "static/uploads/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)

# Ensure templates are auto-reloaded
app.secret_key = "not-so-secret"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def check_extension(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


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
    emotions = db.execute("SELECT * FROM emotion ORDER BY id DESC LIMIT 3")
    exctracted_txt = db.execute("SELECT * FROM image ORDER BY id DESC LIMIT 4")
    similar_texts = db.execute("SELECT * FROM similar ORDER BY id DESC LIMIT 4")
    # extract the text and display it
    return render_template("index.html",
                           emotions=emotions,
                           exctracted_txt=exctracted_txt,
                           similar_texts=similar_texts)


@app.route("/emotion-detection", methods=["GET", "POST"])
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
        return render_template("emotion-detection.html", results=results)

    else:
        # Show last 3 results from DataBase
        results = db.execute("SELECT * FROM emotion ORDER BY id DESC LIMIT 3")
        return render_template("emotion-detection.html", results=results)


# route and function to handle the upload page
@app.route("/text-recognition", methods=["GET", "POST"])
def text_from_image():
    if request.method == "POST":
        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            flash("Image uploaded")

            # Path to image
            img_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            # Getting text from image
            extracted_text = ocr_text(img_path)
            db.execute("INSERT INTO image (image, text) VALUES(?, ?)", img_path, extracted_text)
            results = db.execute("SELECT * FROM image ORDER BY id DESC LIMIT 4")
            return render_template("text-recognition.html",
                                   img_path=img_path,
                                   extracted_text=extracted_text,
                                   results=results)
        else:
            flash("Incorrect type, choose file with extension - png, jpg, jpeg")
            return redirect(request.url)
    else:
        results = db.execute("SELECT * FROM image ORDER BY id DESC LIMIT 4")
        # extract the text and display it
        return render_template("text-recognition.html", results=results)


@app.route("/similar-recognition", methods=["GET", "POST"])
def similar_txt():
    if request.method == "POST":
        # Getting input text into base
        text_1 = request.form.get("text_1")
        text_2 = request.form.get("text_2")
        if not text_1 or not text_2:  # If there is no name, showing erros page
            return render_template("error.html", message="No texts, try again!")

        get_cosine = similarity.processing(text_1, text_2)

        s1_afv = similarity.avg_feature_vector(text_1, model=model,
                                               num_features=100, index2word_set=index2word_set)

        s2_afv = similarity.avg_feature_vector(text_2, model=model,
                                               num_features=100, index2word_set=index2word_set)
        get_cosine_w2v = similarity.cosine_distance(s1_afv, s2_afv)

        # Save it into SQL
        db.execute("INSERT INTO similar (text_1, text_2, score, w2v) VALUES(?, ?, ?, ?)",
                   text_1, text_2, get_cosine, round(float(get_cosine_w2v), 3))

        # Show last 3 results from DataBase
        results = db.execute("SELECT * FROM similar ORDER BY id DESC LIMIT 4")
        return render_template("similar-recognition.html", results=results)
    else:
        # Show last 3 results from DataBase
        results = db.execute("SELECT * FROM similar ORDER BY id DESC LIMIT 4")
        return render_template("similar-recognition.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)