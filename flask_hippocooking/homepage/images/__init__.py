from flask import Blueprint

images = Blueprint('images', __name__)

from . import routes  # Import routes
