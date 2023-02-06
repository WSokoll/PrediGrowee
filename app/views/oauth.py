from datetime import datetime

from flask import Blueprint, current_app, url_for, redirect, flash
from flask_security import login_user
from flask_security.datastore import SQLAlchemyUserDatastore

from app.app import oauth, db
from app.models import User, Role

bp = Blueprint('oauth', __name__)


@bp.route('/login/google', methods=['GET'])
def google():
    oauth.register(
        name='google',
        client_id=current_app.config['GOOGLE_CLIENT_ID'],
        client_secret=current_app.config['GOOGLE_CLIENT_SECRET'],
        server_metadata_url=current_app.config['GOOGLE_CONF_URL'],
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    # Redirect to google_auth function
    redirect_uri = url_for('oauth.google_auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@bp.route('/login/google/callback', methods=['GET'])
def google_auth():
    token = oauth.google.authorize_access_token()
    user_info = token['userinfo']

    # Check if user exists in the database
    user = User.query.filter_by(email=user_info['email']).first()
    if user:
        login_user(user)

        # Logging via Google automatically confirms account
        if user.confirmed_at is None:
            user.confirmed_at = datetime.now()

        db.session.commit()
    else:
        # Register new user
        # TODO: send email (account has been registered - welcome)
        # TODO: flash message
        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        user_datastore.create_user(
            email=user_info['email'],
            password=None,
            confirmed_at=datetime.now(),
            register_only_google=True
        )
        db.session.commit()

        user = User.query.filter_by(email=user_info['email']).first()
        if user:
            login_user(user)
            db.session.commit()
        else:
            flash('An error occurred while trying to register an account using Google.'
                  ' Please try again or use different method to login.', 'error')
            return redirect('security.login')

    return redirect(url_for('welcome.welcome'))
