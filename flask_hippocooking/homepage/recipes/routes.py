from flask import render_template, send_from_directory, current_app, redirect, url_for, abort
from . import recipes
from flask_babel import _, get_locale
import os, sys, json
from ..utils import load_translation_file

@recipes.route('/recipes/<string:recipe_id>', defaults={'locale_id': None})
@recipes.route('/recipes/<string:locale_id>/<string:recipe_id>')
def recipe(recipe_id, locale_id):


    # Detect the preferred locale if it's not provided in the URL
    if locale_id is None:
        # Get the current locale from Flask-Babel's settings
        preferred_locale = str(get_locale())
       
        # Redirect to the same route with the correct locale in the URL
        return redirect(url_for('recipes.recipe', locale_id=preferred_locale, recipe_id=recipe_id))

    # Ensure locale_id matches a supported language
    supported_locales = current_app.config.get('SUPPORTED_LOCALES', ['en', 'fr', 'es', 'de'])  # Example supported locales
    if locale_id not in supported_locales:
        # Fallback to the default locale if the provided one is not supported
        return redirect(url_for('recipes.recipe', locale_id='en', recipe_id=recipe_id))

    

    file_name_recipe = f'{recipe_id}.json'
    file_path_recipe = os.path.join(current_app.root_path, 'static', 'recipes', locale_id, file_name_recipe)

    json_translations_base = load_translation_file((str)(locale_id),'base')

    # Check if the file exists
    if not os.path.exists(file_path_recipe):
        json_translations = {
        "titel": "Recipe Not found",
        }
        return render_template('recipes/not_found.html', translations=json_translations,translations_base=json_translations_base, locale_id=locale_id)
    
    json_translations = load_translation_file((str)(locale_id),'recipes')
   
    # Send the file if it exists
    # json = send_from_directory(os.path.dirname(file_path), file_name, mimetype='application/json')



    with open(file_path_recipe, 'r', encoding='utf-8') as file:
        json_recipe = json.load(file)

    # Return the rendered template
    return render_template('recipes/recipes.html', json_recipe=json_recipe, translations=json_translations, translations_base=json_translations_base, locale_id=locale_id)
