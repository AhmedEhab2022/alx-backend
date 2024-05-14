#!/usr/bin/env python3
""" Module to start a Flask web application
    with babel to handle i18n
"""
from flask import request, render_template, Flask
from flask_babel import Babel


class Config:
    """ Class to set the configuration
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)

app.config.from_object(Config)
babel = Babel(app, locale_selector=get_locale)


@babel.localeselector
def get_locale():
    """ Function to determine the best match with our supported languages.
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def hello_world():
    """ Function to render a template """
    return render_template('2-index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
