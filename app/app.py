from datetime import datetime
from pathlib import Path
from secrets import token_urlsafe

from flask import Flask, render_template
from flask_admin import Admin
from flask_mail import Mail
from flask_security import SQLAlchemyUserDatastore, Security, hash_password
from flask_security.models import fsqla_v2
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth

from app.forms.security import ExtendedRegisterForm, CustomLoginForm
from app.utils.exceptions import exception_handler
from app.views.admin.index import CustomAdminIndexView

db = SQLAlchemy()
admin = Admin(template_mode='bootstrap4', index_view=CustomAdminIndexView())
security = Security()
mail = Mail()
oauth = OAuth()


def create_app():
    app = Flask(
        __name__,
        instance_relative_config=False,
        static_folder='static',
        static_url_path='/static'
    )

    app.config.from_pyfile('config.default.py')
    app.config.from_pyfile('../local/config.local.py')

    app.config["SECURITY_DATETIME_FACTORY"] = datetime.now
    app.config['SQLALCHEMY_DATABASE_URI'] = (f"mysql://{app.config['DB_USER']}:{app.config['DB_PASSWORD']}"
                                             f"@{app.config['DB_HOST']}/{app.config['DB_NAME']}")

    db.init_app(app)

    with app.app_context():
        db.reflect()

    from sqlalchemy import Column, Integer, ForeignKey
    fsqla_v2.FsModels.db = db
    fsqla_v2.FsModels.user_table_name = "user"
    fsqla_v2.FsModels.role_table_name = "role"
    fsqla_v2.FsModels.roles_users = db.Table(
        "roles_users",
        Column("user_id", Integer(), ForeignKey(f"user.id")),
        Column("role_id", Integer(), ForeignKey(f"role.id")),
        extend_existing=True
    )

    mail.init_app(app)
    oauth.init_app(app)

    admin.init_app(app)

    from app.admin import admin_panel_init
    admin_panel_init(admin, db)

    from app.models import User, Role
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)

    security.confirm_register_form = ExtendedRegisterForm
    security.register_form = ExtendedRegisterForm
    security.login_form = CustomLoginForm
    security.init_app(app, user_datastore)

    # Custom 'not found' page
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('custom_error/404.jinja'), 404

    # Custom 'internal server error' page
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('custom_error/500.jinja'), 500

    # Exception handler
    Path(f"{app.root_path}/{app.config['ERROR_LOG']}").touch(exist_ok=True)
    app.register_error_handler(Exception, exception_handler)

    # Admin accounts
    @app.before_first_request
    def db_init():
        if not user_datastore.find_role(role='Admin'):
            db.session.add(Role(name='Admin'))
        if not user_datastore.find_user(email=app.config['ADMIN_EMAIL_1']):
            user_datastore.create_user(
                email=app.config['ADMIN_EMAIL_1'],
                password=hash_password(app.config['ADMIN_PASSWORD_1']),
                confirmed_at=datetime.now(),
                round_token=token_urlsafe(32)[:16],
                roles=['Admin']
            )
        if not user_datastore.find_user(email=app.config['ADMIN_EMAIL_2']):
            user_datastore.create_user(
                email=app.config['ADMIN_EMAIL_2'],
                password=hash_password(app.config['ADMIN_PASSWORD_2']),
                confirmed_at=datetime.now(),
                round_token=token_urlsafe(32)[:16],
                roles=['Admin']
            )
        db.session.commit()

    from app.views.welcome import bp as bp_welcome
    app.register_blueprint(bp_welcome)

    from app.views.oauth import bp as bp_oauth
    app.register_blueprint(bp_oauth)

    from app.views.survey import bp as bp_survey
    app.register_blueprint(bp_survey)

    from app.views.game import bp as bp_game
    app.register_blueprint(bp_game)

    from app.views.results import bp as bp_results
    app.register_blueprint(bp_results)

    from app.views.statistics import bp as bp_statistics
    app.register_blueprint(bp_statistics)

    from app.views.about import bp as bp_about
    app.register_blueprint(bp_about)

    from app.views.contact import bp as bp_contact
    app.register_blueprint(bp_contact)

    return app
