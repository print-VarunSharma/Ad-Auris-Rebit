from flask import Flask, render_template
from flask.templating import render_template_string
import os
from dotenv import load_dotenv
load_dotenv()

# https://realpython.com/flask-by-example-part-1-project-setup/ for deploying with heroku later.
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/home")
def home():
    return render_template("index.html", title="home")

@app.route("/audiowidget")
def audio_widget():
    return render_template("widget_analytics.html", title="audio_widget")

if __name__ == "__main__":
    from waitress import serve
    app.debug = False
    # Turn debug on during local development mode
    port = int(os.environ.get('PORT', 33507))
    waitress.serve(app, port=port)

