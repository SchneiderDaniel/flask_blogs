from flask import Flask, request
import sys
from flask_bootstrap import Bootstrap5
from flask_babel import Babel

bs = Bootstrap5()
babel = Babel()

#Babel
def get_locale():
    # Determine the best match for supported locales
    print("Accepted languages:", request.accept_languages, file=sys.stderr)
    return request.args.get('lang') or request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])


def create_app():
    print('Start creating the app',  file=sys.stderr)
    app = Flask(__name__)

    bs.init_app(app) # Initialize Bootstrap
    print('Bootstrap initialized', file=sys.stderr)

    babel.init_app(app,locale_selector=get_locale, default_translation_directories='translations')
    print('Babel initialized', file=sys.stderr)

    app.config['BABEL_DEFAULT_LOCALE'] = 'de'
    app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'es', 'fr','de']
    

    from homepage.main.routes import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/' )
    from homepage.errors.handlers import errors as errors_blueprint
    app.register_blueprint(errors_blueprint)
    from homepage.recipes.routes import recipes as recipes_blueprint
    app.register_blueprint(recipes_blueprint)
    from homepage.images.routes import images as images_blueprint
    app.register_blueprint(images_blueprint)

    print('Finished creating the app',  file=sys.stderr)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, threaded=True)