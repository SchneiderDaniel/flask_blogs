from flask import render_template, send_from_directory, current_app, redirect, url_for, abort, request, g
from . import recipes
from flask_babel import _, get_locale
import os, sys, json
from ..utils import load_translation_file
import logging

@recipes.before_request
def check_cookie_consent():
    # Check if 'cookieConsentHippocookingcom' cookie is present in the request
    if 'cookieConsentHippocookingcom' in request.cookies:
        # Add any pre-processing logic you want here (e.g., logging or modifying behavior)
        g.cookie_consent = True  # You can use `g` to store data for use in your routes
    else:
        g.cookie_consent = False  # Set `g.cookie_consent` to False if the cookie isn't present


@recipes.route('/recipes/<string:recipe_id>', defaults={'locale_id': None})
@recipes.route('/recipes/<string:locale_id>/<string:recipe_id>')
def recipe(recipe_id, locale_id):
    # Load default locale if none is provided
    if locale_id is None:
        preferred_locale = str(get_locale())
        return redirect(url_for('recipes.recipe', locale_id=preferred_locale, recipe_id=recipe_id))

    # Ensure locale_id matches a supported language
    supported_locales = current_app.config.get('SUPPORTED_LOCALES', ['en', 'fr', 'es', 'de'])
    if locale_id not in supported_locales:
        return redirect(url_for('recipes.recipe', locale_id='en', recipe_id=recipe_id))

    # Initialize translations_base early to ensure it's always available
    json_translations_base = {}
    try:
        json_translations_base = load_translation_file(str(locale_id), 'base')
    except Exception as e:
        logging.error(f"Error loading base translations: {str(e)}")
        json_translations_base = {"error": "Base translations unavailable"}

    # Build the file path for the recipe
    file_name_recipe = f'{recipe_id}.json'
    file_path_recipe = os.path.join(current_app.root_path, 'static', 'recipes', locale_id, file_name_recipe)

    # Check if the recipe file exists
    if not os.path.exists(file_path_recipe):
        logging.error(f"Recipe file not found: {file_path_recipe}")
        json_translations = {"titel": "Recipe Not Found"}
        return render_template(
            'recipes/not_found.html',
            translations=json_translations,
            translations_base=json_translations_base,  # Ensure this is passed
            locale_id=locale_id,
            cookie_consent=g.cookie_consent
        ), 404

    # Attempt to load recipe file
    try:
        with open(file_path_recipe, 'r', encoding='utf-8') as file:
            json_recipe = json.load(file)
    except (json.JSONDecodeError, IOError) as e:
        logging.error(f"Error reading recipe file {file_path_recipe}: {str(e)}")
        abort(500, description="An error occurred while processing the recipe file.")

    # Load additional translations
    try:
        json_translations = load_translation_file(str(locale_id), 'recipes')
    except Exception as e:
        logging.error(f"Error loading recipe translations: {str(e)}")
        json_translations = {"error": "Recipe translations unavailable"}

    # Render the recipe template
    return render_template(
        'recipes/recipes.html',
        json_recipe=json_recipe,
        recipe_id=recipe_id,
        translations=json_translations,
        translations_base=json_translations_base,  # Ensure this is passed
        locale_id=locale_id,
        cookie_consent=g.cookie_consent
    )

