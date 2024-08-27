#!/usr/bin/env python3
""" Basic flask app """
from flask import Flask, render_template, request
from flask_babel import Babel, _


class Config:
    """ Flask Babel Configuration """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


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
    return render_template('4-index.html', locale=locale)


if __name__ == "__main__":
    app.run(debug=True)
