from flask import Blueprint, render_template
from ..utils import load_translation_file

errors = Blueprint('errors', __name__)

# Default error translations
data = {
    "titel": "Error",
}

def load_base_translations():
    """Helper function to load base translations with a fallback."""
    try:
        return load_translation_file('en', 'base')  # Load 'base' translations for the 'en' locale
    except Exception as e:
        # Fallback to default content if loading fails
        print(f"Error loading base translations: {e}")
        return {"cookietext": "We use cookies to improve your experience."}


@errors.app_errorhandler(404)
def error404(error):
    json_translations_base = load_base_translations()
    return render_template(
        'errors/404.html',
        translations=data,
        translations_base=json_translations_base,
        locale_id="en"
    ), 404


@errors.app_errorhandler(403)
def error403(error):
    json_translations_base = load_base_translations()
    return render_template(
        'errors/403.html',
        translations=data,
        translations_base=json_translations_base,
        locale_id="en"
    ), 403


@errors.app_errorhandler(500)
def error500(error):
    json_translations_base = load_base_translations()
    return render_template(
        'errors/500.html',  # Use a specific 500.html template if available
        translations=data,
        translations_base=json_translations_base,
        locale_id="en"
    ), 500
