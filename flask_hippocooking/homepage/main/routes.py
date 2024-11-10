from flask import render_template, send_from_directory, current_app, url_for, redirect,request
from flask_babel import _, get_locale
from . import main
import os



@main.route('/', defaults={'locale_id': None})
@main.route('/<string:locale_id>')
def index(locale_id):
    
    print("Start Index")
    
    # Detect the preferred locale if it's not provided in the URL
    if locale_id is None:
        print("isNone")
        # Get the current locale from Flask-Babel's settings
        preferred_locale = str(get_locale())
        print("language:" + preferred_locale)
        # Redirect to the same route with the correct locale in the URL
        return redirect(url_for('main.index', locale_id=preferred_locale))

     # Ensure `locale_id` is one of the supported locales
    if locale_id not in current_app.config['BABEL_SUPPORTED_LOCALES']:
        print("isNot supported")
        # If the locale_id is not supported, redirect to the preferred locale
        return redirect(url_for('main.index', locale_id=str(get_locale())))

    print("Render")
    return render_template('main/index.html', title='Blog')

@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'), 'resources/icons/favicon.ico', mimetype='image/vnd.microsoft.icon')

@main.route('/about')
def about():
    return render_template('main/about.html', title='Über uns')

