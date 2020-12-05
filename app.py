from flask import Flask, render_template, url_for, jsonify, request, send_from_directory, redirect
from flask.templating import render_template_string
import os
from dotenv import load_dotenv
load_dotenv()
"""
This app.py file is the main backend code that flask runs on. Mainly initiates the flask hosting, and the main routes.
App.py will not run correctly if project file structure is not in an appropiate format for flask. Ensure static, templates, etc folders are in proper form.

"""

# https://realpython.com/flask-by-example-part-1-project-setup/ for deploying with heroku later.
app = Flask(__name__, static_url_path='/static')
app.config['JSON_AS_ASCII'] = False


# --------------------- Main Routes ------------------------------------------


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/test_widget")
def test_widget():
    return render_template("test_widget.html", title="test_widget")

# --------------------- Rebit ------------------------------------------

"""
This route is a highly important route as it is running Rebit's first live widget that is collecting data through GTM.
"""
@app.route('/rebit_cyberpulse_nov')
def audio_widget_1():
    return render_template('rebit_cyberpulse_nov.html')


@app.route('/rebit_cyberpulse_dec')
def audio_widget_2():
    return render_template('rebit/cyberpulse-dec.html')

# --------------------- Abiltiy Magazine ------------------------------------------


@app.route('/ability-magazine/a-doll-like-me')
def audio_widget_3():
    return render_template('scomingsoon.html')


@app.route('/ability-magazine/interview-with-mandy-harvey')
def audio_widget_4():
    return render_template('comingsoon.html')


@app.route('/ability-magazine/interview-with-nancy-silberkleit-ceo-of-archie-comics-co/')
def audio_widget_5():
    return render_template('comingsoon.html')


@app.route('/ability-magazine/ian-harding')
def audio_widget_6():
    return render_template('comingsoon.html')


@app.route('/ability-magazine/the-wikipedia-foundation')
def audio_widget_7():
    return render_template('comingsoon.html')


@app.route('/ability-test')
def audio_widget_ability():
    return render_template('ability-test.html')


# @app.route('/ability-magazine/<article_name>')
# def article_slug(article_name):
#     return(HTML_TEMPLATE.substitute(article_url_name=article_name))

# --------------------- WomenLead ------------------------------------------
@app.route('/womenlead_1')
def audio_widget_8():
    return render_template('/womenlead_1.html')

if __name__ == "__main__":
    app.debug = False
    from waitress import serve
    # Turn debug on during local development mode
    port = int(os.environ.get('PORT', 33507))
    waitress.serve(app, port=port)

