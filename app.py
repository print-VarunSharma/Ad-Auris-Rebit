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
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import traceback
import json
import psycopg2
from flask_heroku import Heroku
import os.path


"""
This app.py file is the main backend code that flask runs on. Mainly initiates the flask hosting, and the main routes.
App.py will not run correctly if project file structure is not in an appropiate format for flask. Ensure static, templates, etc folders are in proper form.

"""

# https://realpython.com/flask-by-example-part-1-project-setup/ for deploying with heroku later.

app = Flask(__name__, static_url_path='/static')
app.config['JSON_AS_ASCII'] = False
app.config.from_object('config')
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

# ------------------- DATABASE CONFIGS -----------------------------------------
"""
Database Config initializes the Dynamic Database and allows for context switching due to the inaccessibility of HerokuPostgreSQL in local development. Dev DB uses SQL Lite, and Production DB uses HerokuPostgreSQL.

"""
ENV = 'prod'

DATABASE_URL = os.getenv("DATABASE_URL")
heroku = Heroku(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
basedir = os.path.abspath(os.path.dirname(__file__))

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite3')
else: 
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://ugcaiyuvhyyfci:14ad4abd5b5aa3f8567aa530a3a92f204644e6b514e2ffd21eff606aeda96226@ec2-23-20-205-19.compute-1.amazonaws.com:5432/d1mf5k5it0la2"
    # conn = psycopg2.connect(DATABASE_URL,sslmode='require')

db = SQLAlchemy(app)

# -------------------  DATABASE CONFIGS ----------------------------------------

# --------------------- Database Logs ------------------------------------------
"""
Database Logs - logs all the production logs for requests and errors. 

"""
class Log(db.Model):
    __tablename__ = 'ad-auris-narrations-audiowidget-logs'
    id = db.Column(db.Integer, primary_key=True) # auto incrementing
    logger = db.Column(db.String(100)) # the name of the logger. (e.g. myapp.views)
    level = db.Column(db.String(100)) # info, debug, or error?
    trace = db.Column(db.String(4096)) # the full traceback printout
    msg = db.Column(db.String(4096)) # any custom log you may have included
    created_at = db.Column(db.DateTime, default=db.func.now()) # the current timestamp

    def __init__(self, logger=None, level=None, trace=None, msg=None):
        self.logger = logger
        self.level = level
        self.trace = trace
        self.msg = msg

    def __unicode__(self):
        return self.__repr__()

    def __repr__(self):
        return "<Log: %s - %s>" % (self.created_at.strftime('%m/%d/%Y-%H:%M:%S'), self.msg[:50])


class SQLAlchemyHandler(logging.Handler):
    
    def emit(self, record):
        trace = None
        exc = record.__dict__['exc_info']
        if exc:
            trace = traceback.format_exc()
        log = Log(
            logger=record.__dict__['name'],
            level=record.__dict__['levelname'],
            trace=trace,
            msg=record.__dict__['msg'],)
        db.session.add(log)
        db.session.commit()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ch = SQLAlchemyHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)



loggers = [logger, logging.getLogger('werkzeug'),  logging.getLogger('sqlalchemy'), logging.getLogger('flask.app')]

for l in loggers:
    l.addHandler(ch)

csrf = CSRFProtect()
db.create_all()

# --------------------- Developement Logs ------------------------------------------
"""
Development Logs - logs all the development logs for all requests and errors. It is organized and color coded for optimizing visual ques.

"""
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

# --------------------- Error Handling ------------------------------------------
"""
Error Handling - Handles 400 level and 500 level errors and redirects to a pre-set template for the user.
User can push a button to go back. This prevents the application from breaking and for opimizing user journey.

"""
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
"""
Main Routes - All app routing is executed from here. All live widgets deployed on customer websites are using these specified URLs.

"""

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

 # --------------------- App Configs & Settings ------------------------------------------

"""
App Configs & Settings - This compiles the app in a desired way for dev and prod. 

@app.run: Debug must be True during dev and False for prod.

@app.run: Threading must be on to handle a multitude of requests at once.

@app.logger: Handles Gunicorn production logging outside of Heroku logs

"""
if __name__ == "__main__":
    # Dev - Prod Settings
        # Turn debug on during local development mode
    app.run(debug=False, threaded=True)
    from waitress import serve

    # Gunicorn Production Logging
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    # Database init
    csrf.init_app(app)
    logger.critical('TEST CRITICAL ERROR')

    port = int(os.environ.get('PORT', 33507))
    waitress.serve(app, port=port)
