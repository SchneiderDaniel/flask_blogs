# save this as app.py
from flask import Flask
import sys


def create_app():
    print('Start creating the app',  file=sys.stderr)
    app = Flask(__name__)
    
    from homepage.main.routes import main
    app.register_blueprint(main, url_prefix='/' )

    print('Finished creating the app',  file=sys.stderr)

    return app