#!/usr/bin/env python3
""" Basic flask app """
from flask import Flask, render_template, request, g
from flask_babel import Babel, _
import pytz
from pytz.exceptions import UnknownTimeZoneError
from datetime import datetime
from flask_babel import format_datetime


class Config:
    """ Flask Babel Configuration """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """ Retrieve user by ID from URL """
    usr_id = request.args.get('login_as', type=int)
    return users.get(usr_id)


@app.before_request
def before_request():
    """ Set the current user before each request """
    g.user = get_user()


@babel.localeselector
def get_locale():
    """ Determines the best match with the supported langs """
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale

    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']

    hlocale = request.headers.get('locale', '')
    if hlocale in app.config['LANGUAGES']:
        return hlocale

    return request.accept_languages.best_match(
            app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """ Retrieves and validates timezeone """
    tz = request.args.get('timezone', '').strip()
    if not tz and g.user:
        tz = g.user['timezone']

    try:
        return pytz.timezone(tz).zone
    except UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/', strict_slashes=False)
def index_page():
    """ Renders index page """
    locale = get_locale()
    timezone = get_timezone()
    now = datetime.now(pytz.timezone(timezone))
    formatted_time = format_datetime(now)

    return render_template('index.html', locale=locale,
                           timezone=timezone,
                           current_time=formatted_time)


if __name__ == "__main__":
    app.run(debug=True)
