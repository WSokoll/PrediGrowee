from flask import Flask


def create_app():
    app = Flask(
        __name__,
        instance_relative_config=False,
        static_folder='static',
        static_url_path='/static'
    )

    app.config.from_pyfile('config.default.py')
    app.config.from_pyfile('../local/config.local.py')

    from app.views.welcome import bp as bp_welcome
    app.register_blueprint(bp_welcome)

    from app.views.login import bp as bp_login
    app.register_blueprint(bp_login)

    return app
