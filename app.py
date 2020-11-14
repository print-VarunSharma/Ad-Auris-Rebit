from flask import Flask, render_template, url_for, jsonify, request, send_from_directory, redirect
from flask.templating import render_template_string
import os
from dotenv import load_dotenv
load_dotenv()
# Azure imports
import translate, sentiment, synthesize


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
    app.debug = False
    from waitress import serve
    # Turn debug on during local development mode
    port = int(os.environ.get('PORT', 33507))
    waitress.serve(app, port=port)

