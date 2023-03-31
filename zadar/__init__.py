import os

from flask import Flask

# creating virtual env
# py -m venv env

# activate virtual environment
# .\env\Scripts\activate

# run app debugger
# flask --app zadar run --debug

# init db
# flask --app zadar init-db

# This function is the application factory that creates
# and returns a new Flask application.


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='as7fbd7ad9asd5cvxc9ds023238235hdsf81329df',
        DATABASE=os.path.join(app.instance_path, 'zadar.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db

    # initializes the Flask application with the database
    # configuration
    db.init_app(app)

    from .blueprints import auth
    app.register_blueprint(auth.bp)

    from .blueprints import posts
    app.register_blueprint(posts.bp)
    app.add_url_rule('/', endpoint='index')

    from .blueprints import tempedia
    app.register_blueprint(tempedia.bp)

    from .blueprints import techniques
    app.register_blueprint(techniques.bp)

    from .blueprints import type_chart
    app.register_blueprint(type_chart.bp)

    from .blueprints import traits
    app.register_blueprint(traits.bp)

    from .blueprints import about
    app.register_blueprint(about.bp)

    from .blueprints import patch
    app.register_blueprint(patch.bp)

    from .blueprints import weaknesses_calculator
    app.register_blueprint(weaknesses_calculator.bp)

    return app