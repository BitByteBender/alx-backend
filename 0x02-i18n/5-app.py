#!/usr/bin/env python3
""" Basic flask app """
from flask import Flask, render_template, request, g
from flask_babel import Babel, _


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
    return request.accept_languages.best_match(
            app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def index_page():
    """ Renders index page """
    locale = get_locale()
    return render_template('5-index.html', locale=locale)


if __name__ == "__main__":
    app.run(debug=True)
