from flask import render_template, send_from_directory, current_app, url_for, redirect
from flask_babel import _, get_locale
from . import main
import os, json
from ..utils import load_translation_file, count_json_files


@main.route('/', defaults={'locale_id': None})
@main.route('/<string:locale_id>')
def index(locale_id):
    
    # Detect the preferred locale if it's not provided in the URL
    if locale_id is None:
        # Get the current locale from Flask-Babel's settings
        preferred_locale = str(get_locale())
        # Redirect to the same route with the correct locale in the URL
        return redirect(url_for('main.index', locale_id=preferred_locale))

     # Ensure `locale_id` is one of the supported locales
    if locale_id not in current_app.config['BABEL_SUPPORTED_LOCALES']:
        # If the locale_id is not supported, redirect to the preferred locale
        return redirect(url_for('main.index', locale_id=str(get_locale())))

    
    file_path_index = os.path.join(current_app.root_path, 'static', 'translations', locale_id, "index.json")
   
    # Check if the file exists
    if not os.path.exists(file_path_index):
        json_translations = {
        "titel": "Translation Not found",
        }
        return render_template('recipes/not_found.html', translations=json_translations, locale_id=locale_id)

    json_translations = load_translation_file((str)(locale_id),'index')


    folder_path = os.path.join(current_app.root_path, 'static', 'recipes', locale_id)
    number_of_recipes = count_json_files(folder_path)*100


    return render_template('main/index.html', translations=json_translations, locale_id=locale_id, number_of_recipes=number_of_recipes)


@main.route('/about', defaults={'locale_id': None})
@main.route('/<string:locale_id>/about')
def about(locale_id):
    json_translations = load_translation_file((str)(locale_id),'about')
    return render_template('main/about.html',translations=json_translations, locale_id=locale_id)


@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'), 'resources/icons/favicon.ico', mimetype='image/vnd.microsoft.icon')



