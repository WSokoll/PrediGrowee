from flask import Blueprint, render_template, current_app, url_for, redirect

from app.app import oauth

bp = Blueprint('login', __name__)


@bp.route('/login', methods=['GET'])
def login():
    return render_template('login.jinja')


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
    redirect_uri = url_for('login.google_auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@bp.route('/login/google/auth', methods=['GET'])
def google_auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    print(" Google User ", user)
    return redirect(url_for('welcome.welcome'))
