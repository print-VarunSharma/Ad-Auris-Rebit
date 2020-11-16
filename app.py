from flask import Flask, render_template, url_for, jsonify, request, send_from_directory, redirect, flash
from flask.templating import render_template_string
import os
from dotenv import load_dotenv
load_dotenv()
# Azure imports
import translate, sentiment, synthesize

# from flask_mail import Message, Mail
# return redirect("http://www.example.com", code=302)


# https://realpython.com/flask-by-example-part-1-project-setup/ for deploying with heroku later.
app = Flask(__name__, static_url_path='/static')
app.config['JSON_AS_ASCII'] = False

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
                                                  
@app.route("/")
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/test_widget")
def test_widget():
    return render_template("test_widget.html", title="test_widget")

@app.route("/rebit_1")
def rebit_1():
    return render_template("rebit_1.html", title="audio_widget")


@app.route('/rebit_2')
def rebit_2():
    return render_template('rebit_2.html')


@app.route('/rebit_3')
def rebit_3():
    return render_template('rebit_3.html')

@app.route('/rebit_4')
def rebit_4():
    return render_template('rebit_4.html')

@app.route('/rebit_5')
def rebit_5():
    return render_template('rebit_5.html')

@app.route('/rebit_6')
def rebit_6():
    return render_template('rebit_6.html')

@app.route('/rebit_cyberpulse_nov')
def rebit_cyberpulse_nov():
    return render_template('rebit_cyberpulse_nov.html')


# from flask_mail import Mail, Message

# mail = Mail()
# SECRET_KEY = os.getenv("SECRET_KEY")
# app.secret_key = SECRET_KEY
# MAIL_SERVER = os.getenv("MAIL_SERVER")
# MAIL_PORT = os.getenv("MAIL_PORT")
# MAIL_USERNAME = os.getenv("MAIL_USERNAME")
# MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

# app.config["MAIL_SERVER"] = MAIL_SERVER
# app.config["MAIL_PORT"] = MAIL_PORT
# app.config["MAIL_USE_SSL"] = True
# app.config["MAIL_USERNAME"] = MAIL_USERNAME
# app.config["MAIL_PASSWORD"] = MAIL_PASSWORD

# mail.init_app(app)
# ---------------------------------------Contact----------------------------------
# @app.route('/contact', methods=['GET', 'POST'])
# def contact():
#   form = ContactForm()
 
#   if request.method == 'POST':
#     if form.validate() == False:
#       flash('All fields are required.')
#       return render_template('contact.html', form=form)
#     else:
#       msg = Message(form.subject.data, sender='contact@example.com', recipients=['your_email@example.com'])
#       msg.body = """
#       From: %s &lt;%s&gt;
#       %s
#       """ % (form.name.data, form.email.data, form.message.data)
#       mail.send(msg)
 
#       return render_template('contact.html', success=True)
 
#   elif request.method == 'GET':
#     return render_template('contact.html', form=form)

# from wtforms import validators
# from wtforms import Form, TextAreaField, SubmitField, validators, TextField, BooleanField
# from wtforms.validators import Required, Email
# class ContactForm(Form):
#     name = TextField("Name",  [validators.Required("Please enter your name.")])
#     email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
#     subject = TextField("Subject",  [validators.Required("Please enter a subject.")])
#     message = TextAreaField("Message",  [validators.Required("Please enter a message.")])
#     submit = SubmitField("Send")
# #------------------------------------Feedback-----------------------------------------
# from flask_wtf import FlaskForm
# from wtforms import StringField, TextField, SubmitField
# from wtforms.validators import DataRequired, Length
# from forms import ContactForm
# @app.route('/feedback', methods=('GET', 'POST'))
# def feedback():
#     form = ContactForm()
#     if form.validate_on_submit():
#         return redirect(url_for('success'))
#     return render_template('feedback.html', form=form)


# --------------------- Azure Cognitive Services ------------------------------------------
@app.route('/azureservices')
def index():
    return render_template('azure.html')

@app.route('/translate-text', methods=['POST'])
def translate_text():
    data = request.get_json()
    text_input = data['text']
    translation_output = data['to']
    response = translate.get_translation(text_input, translation_output)
    return jsonify(response)

@app.route('/sentiment-analysis', methods=['POST'])
def sentiment_analysis():
    data = request.get_json()
    input_text = data['inputText']
    input_lang = data['inputLanguage']
    output_text = data['outputText']
    output_lang =  data['outputLanguage']
    response = sentiment.get_sentiment(input_text, input_lang, output_text, output_lang)
    return jsonify(response)


@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    data = request.get_json()
    text_input = data['text']
    voice_font = data['voice']
    tts = synthesize.TextToSpeech(text_input, voice_font)
    tts.get_token()
    audio_response = tts.save_audio()
    return audio_response


if __name__ == "__main__":
    app.debug = True
    from waitress import serve
    # Turn debug on during local development mode
    port = int(os.environ.get('PORT', 33507))
    waitress.serve(app, port=port)

