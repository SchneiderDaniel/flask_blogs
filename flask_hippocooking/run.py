from flask import Flask
import sys
from flask_bootstrap import Bootstrap5

bs = Bootstrap5()


def create_app():
    print('Start creating the app',  file=sys.stderr)
    app = Flask(__name__)

    bs.init_app(app) # Initialize Bootstrap
    print('Bootstrap initialized', file=sys.stderr)

    from homepage.main.routes import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/' )
    from homepage.errors.handlers import errors as errors_blueprint
    app.register_blueprint(errors_blueprint)

    print('Finished creating the app',  file=sys.stderr)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, threaded=True)