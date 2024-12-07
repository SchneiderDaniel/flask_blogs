from flask import render_template, send_from_directory, current_app, url_for, redirect, Response,request, g
from flask_babel import _, get_locale
from . import main
import os, json
from ..utils import load_translation_file, count_json_files


@main.before_request
def check_cookie_consent():
    # Check if 'cookieConsentHippocookingcom' cookie is present in the request
    if 'cookieConsentHippocookingcom' in request.cookies:
        # Add any pre-processing logic you want here (e.g., logging or modifying behavior)
        g.cookie_consent = True  # You can use `g` to store data for use in your routes
    else:
        g.cookie_consent = False  # Set `g.cookie_consent` to False if the cookie isn't present


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


    json_translations_base = load_translation_file((str)(locale_id),'base')
    
    file_path_index = os.path.join(current_app.root_path, 'static', 'translations', locale_id, "index.json")
   
    # Check if the file exists
    if not os.path.exists(file_path_index):
        json_translations = {
        "titel": "Translation Not found",
        }
        return render_template('recipes/not_found.html', translations=json_translations,translations_base=json_translations_base, locale_id=locale_id, cookie_consent=g.cookie_consent)

    json_translations = load_translation_file((str)(locale_id),'index')


    folder_path = os.path.join(current_app.root_path, 'static', 'recipes', locale_id)
    number_of_recipes = count_json_files(folder_path)*100

    folder_path = os.path.join(current_app.root_path, 'static', 'recipes', locale_id)

    # List to store the JSON data
    json_data = []

    # Check if the directory exists, and then loop through the JSON files in the folder
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith('.json'):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    try:
                        data = json.load(file)
                        json_data.append(data)
                    except json.JSONDecodeError:
                        continue  # Skip files that are not valid JSON
    else:
        # If the folder does not exist, you might want to handle the error here
        return f"Folder {folder_path} not found.", 404

    
    return render_template('main/index.html', translations=json_translations, translations_base=json_translations_base, locale_id=locale_id, number_of_recipes=number_of_recipes,json_files=json_data, cookie_consent=g.cookie_consent)


@main.route('/about', defaults={'locale_id': None})
@main.route('/<string:locale_id>/about')
def about(locale_id):

     # Detect the preferred locale if it's not provided in the URL
    if locale_id is None:
        # Get the current locale from Flask-Babel's settings
        preferred_locale = str(get_locale())
        # Redirect to the same route with the correct locale in the URL
        return redirect(url_for('main.about', locale_id=preferred_locale))

    json_translations = load_translation_file((str)(locale_id),'about')
    json_translations_base = load_translation_file((str)(locale_id),'base')
    return render_template('main/about.html',translations=json_translations, locale_id=locale_id, translations_base=json_translations_base, cookie_consent=g.cookie_consent)

@main.route('/impressum', defaults={'locale_id': None})
@main.route('/<string:locale_id>/impressum')
def impressum(locale_id):

     # Detect the preferred locale if it's not provided in the URL
    if locale_id is None:
        # Get the current locale from Flask-Babel's settings
        preferred_locale = str(get_locale())
        # Redirect to the same route with the correct locale in the URL
        return redirect(url_for('main.impressum', locale_id=preferred_locale))

    json_translations = load_translation_file((str)(locale_id),'impressum')
    json_translations_base = load_translation_file((str)(locale_id),'base')
    return render_template('main/impressum.html',translations=json_translations, locale_id=locale_id, translations_base=json_translations_base, cookie_consent=g.cookie_consent)

@main.route('/dataprotection', defaults={'locale_id': None})
@main.route('/<string:locale_id>/dataprotection')
def dataprotection(locale_id):

     # Detect the preferred locale if it's not provided in the URL
    if locale_id is None:
        # Get the current locale from Flask-Babel's settings
        preferred_locale = str(get_locale())
        # Redirect to the same route with the correct locale in the URL
        return redirect(url_for('main.dataprotection', locale_id=preferred_locale))

    json_translations = load_translation_file((str)(locale_id),'dataprotection')
    json_translations_base = load_translation_file((str)(locale_id),'base')
    return render_template('main/dataprotection.html',translations=json_translations, locale_id=locale_id, translations_base=json_translations_base, cookie_consent=g.cookie_consent)



@main.route('/alive')
def alive():
    locale_id = str(get_locale())
    json_translations = load_translation_file((str)(locale_id),'dataprotection')
    json_translations_base = load_translation_file((str)(locale_id),'base')
    return render_template('main/alive.html', translations=json_translations, translations_base=json_translations_base, cookie_consent=g.cookie_consent)

@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'), 'resources/icons/favicon.ico', mimetype='image/vnd.microsoft.icon')

@main.route('/robots.txt')
def robots_txt():
    return send_from_directory(os.path.join(current_app.root_path, 'static'), 'others/robots.txt')

@main.route('/sitemap.xml')
def sitemap_xml():
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    # Get array of locale
    locale_array = current_app.config['BABEL_SUPPORTED_LOCALES']
    for locale in locale_array:
        # Load recipes per locale

        recipe_array = []
        folder_path = os.path.join(current_app.root_path, 'static', 'recipes', locale)
        if os.path.exists(folder_path):
            for filename in os.listdir(folder_path):
                if filename.endswith('.json'):
                    name, _ = os.path.splitext(filename)
                    recipe_array.append(name)

        for recipe in recipe_array:
            # Add default recipe URL
            xml.append("<url>")
            xml.append(f"<loc>https://hippocooking.com/recipes/{locale}/{recipe}</loc>")
            xml.append("<changefreq>weekly</changefreq>")
            xml.append("<priority>0.9</priority>")
            xml.append("</url>")

        xml.append("<url>")
        xml.append(f"<loc>https://hippocooking.com/{locale}</loc>")
        xml.append("<changefreq>weekly</changefreq>")
        xml.append("<priority>0.8</priority>")
        xml.append("</url>")

        xml.append("<url>")
        xml.append(f"<loc>https://hippocooking.com/{locale}/about</loc>")
        xml.append("<changefreq>weekly</changefreq>")
        xml.append("<priority>0.7</priority>")
        xml.append("</url>")

    xml.append('</urlset>')
    return Response("\n".join(xml), mimetype='application/xml')

