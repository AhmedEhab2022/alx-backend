#!/usr/bin/env python3
""" Module to start a Flask web application
    with babel to handle i18n
"""
from flask import request, render_template, Flask
from flask_babel import Babel, _, g
from pytz import timezone as timezoneFunc, exceptions


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """ Class to set the configuration
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)

app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """ Function to determine the best match with our supported languages.
    """
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user.get('locale')
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user():
    """ Function to get a user
    """
    user_id = request.args.get('login_as')
    try:
        return users.get(int(user_id))
    except Exception:
        return None


@app.before_request
def before_request():
    """ Function to get a user
    """
    user = get_user()
    g.user = user


@babel.timezoneselector
def get_timezone():
    """ Function to determine the best match with our supported timezone.
    """
    timezone = request.args.get('timezone')
    if timezone:
        try:
            return timezoneFunc(timezone)
        except exceptions.UnknownTimeZoneError:
            pass
    if g.user and g.user.get('timezone'):
        try:
            return timezoneFunc(g.user.get('timezone'))
        except exceptions.UnknownTimeZoneError:
            pass
    return timezoneFunc(app.config['BABEL_DEFAULT_TIMEZONE'])


@app.route('/', strict_slashes=False)
def hello_world():
    """ Render the main template """
    return render_template('7-index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
