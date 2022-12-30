from datetime import datetime

from flask import Flask
from flask_mail import Mail
from flask_security import SQLAlchemyUserDatastore, Security
from flask_security.models import fsqla_v2
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth

from app.forms.security import ExtendedRegisterForm

db = SQLAlchemy()
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

    from app.models import User, Role
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)

    security.confirm_register_form = ExtendedRegisterForm
    security.init_app(app, user_datastore)

    from app.views.welcome import bp as bp_welcome
    app.register_blueprint(bp_welcome)

    from app.views.oauth import bp as bp_oauth
    app.register_blueprint(bp_oauth)

    return app
