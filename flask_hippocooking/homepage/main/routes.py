from flask import render_template, send_from_directory, current_app
from . import main
import os

@main.route('/')
def index():
     return render_template('main/index.html', title='Blog')

@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'), 'resources/icons/favicon.ico', mimetype='image/vnd.microsoft.icon')


@main.route('/about')
def about():
    return render_template('main/about.html', title='Über uns')