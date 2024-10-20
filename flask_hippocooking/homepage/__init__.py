# save this as app.py
from flask import Flask


def create_app(config_class=Config):
    print('Start creating the app',  file=sys.stderr)
    app = Flask(__name__)
    print('Start configure the app',  file=sys.stderr)
    app.config.from_object(Config)
    
    from homepage.main.routes import main
    app.register_blueprint(main)

    
    print('Finished creating the app',  file=sys.stderr)