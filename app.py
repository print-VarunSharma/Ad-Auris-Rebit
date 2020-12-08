from flask import Flask, render_template, url_for, jsonify, request, send_from_directory, redirect
from flask.templating import render_template_string
import os
from dotenv import load_dotenv
load_dotenv()

import datetime
import time
import colors
from flask import g, request
from rfc3339 import rfc3339
import logging
"""
This app.py file is the main backend code that flask runs on. Mainly initiates the flask hosting, and the main routes.
App.py will not run correctly if project file structure is not in an appropiate format for flask. Ensure static, templates, etc folders are in proper form.

"""

# https://realpython.com/flask-by-example-part-1-project-setup/ for deploying with heroku later.
app = Flask(__name__, static_url_path='/static')
app.config['JSON_AS_ASCII'] = False


@app.before_request
def start_timer():
    g.start = time.time()


@app.before_request
def start_timer():
    g.start = time.time()


@app.after_request
def log_request(response):
    if request.path == '/favicon.ico':
        return response
    elif request.path.startswith('/static'):
        return response

    now = time.time()
    duration = round(now - g.start, 2)
    dt = datetime.datetime.fromtimestamp(now)
    timestamp = rfc3339(dt, utc=True)

    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    host = request.host.split(':', 1)[0]
    args = dict(request.args)

    log_params = [
        ('method', request.method, 'blue'),
        ('path', request.path, 'blue'),
        ('status', response.status_code, 'yellow'),
        ('duration', duration, 'green'),
        ('time', timestamp, 'magenta'),
        ('ip', ip, 'red'),
        ('host', host, 'red'),
        ('params', args, 'blue')
    ]

    request_id = request.headers.get('X-Request-ID')
    if request_id:
        log_params.append(('request_id', request_id, 'yellow'))

    parts = []
    for name, value, color in log_params:
        part = colors.color("{}={}".format(name, value), fg=color)
        parts.append(part)
    line = " ".join(parts)

    app.logger.info(line)

    return response

@app.errorhandler(404) 
# inbuilt function which takes error as parameter 
def not_found(e): 
    print(e)
# defining function 
    return render_template("404.html") 

@app.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    print(e)
    return render_template('500.html'), 500
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


@app.route('/rebit/cyberpulse-dec')
def audio_widget_2():
    return render_template('rebit-cyberpulse-dec.html')

# --------------------- Abiltiy Magazine ------------------------------------------


@app.route('/ability-magazine/a-doll-like-me')
def audio_widget_3():
    return render_template('ability-magazine-a-doll-like-me.html')


@app.route('/ability-magazine/interview-with-mandy-harvey')
def audio_widget_4():
    return render_template('ability-magazine-interview-with-mandy-harvey.html')


@app.route('/ability-magazine/interview-with-nancy-silberkleit-ceo-of-archie-comics-co/')
def audio_widget_5():
    return render_template('ability-magazine-interview-with-nancy-silberkleit-ceo-of-archie-comics-co.html')


@app.route('/ability-magazine/ian-harding')
def audio_widget_6():
    return render_template('ability-magazine-ian-harding.html')


@app.route('/ability-magazine/the-wikipedia-foundation')
def audio_widget_7():
    return render_template('ability-magazine-the-wikipedia-foundation.html')


@app.route('/ability-test')
def audio_widget_ability():
    return render_template('ability-test.html')

@app.route('/ability-magazine/veronika')
def audio_widget_ability_testV2():
    return render_template('/ability-magazine-veronika.html')

    
# @app.route('/test/<string: article_name>')
# def article_slug(article_name):
#      return(HTML_TEMPLATE.substitute(article_url_name=article_name))

# --------------------- WomenLead ------------------------------------------
@app.route('/womenlead_1')
def audio_widget_8():
    return render_template('/womenlead_1.html')

if __name__ == "__main__":
    app.debug = False
    app.run(threaded=True)
    from waitress import serve
    # Turn debug on during local development mode
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    port = int(os.environ.get('PORT', 33507))
    waitress.serve(app, port=port)
