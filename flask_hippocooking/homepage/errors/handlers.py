from flask import Blueprint, render_template


errors = Blueprint('errors', __name__)

data = {
        "titel": "Error",
}

@errors.app_errorhandler(404)
def error404(error):
    return render_template('errors/404.html', translations=data, locale_id="en"), 404


@errors.app_errorhandler(403)
def error403(error):
    return render_template('errors/403.html', translations=data, locale_id="en"), 403


@errors.app_errorhandler(500)
def error500(error):
    return render_template('errors/404.html', translations=data, locale_id="en"), 500