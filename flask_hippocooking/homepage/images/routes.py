from flask import render_template, send_from_directory, current_app, url_for, redirect, abort
from flask_babel import _, get_locale
from . import images
from ..utils import load_translation_file, count_json_files


@images.route('/images/<image_id>.jpg')
def serve_image(image_id):
    # Ensure the ID is valid (e.g., a 5-digit number)
    if len(image_id) != 5 or not image_id.isdigit():
        abort(404)  # Return a 404 if the ID is invalid

    # Define the directory where images are stored
    image_directory = 'static/resources/images'

    # Attempt to serve the image
    try:
        return send_from_directory(image_directory, f"{image_id}.jpg")
    except FileNotFoundError:
        abort(404)  # Return a 404 if the image doesn't exist