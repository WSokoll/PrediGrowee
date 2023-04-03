from flask import Blueprint, render_template, current_app

bp = Blueprint('contact', __name__)


@bp.route('/contact', methods=['GET'])
def get():
    contact_email = current_app.config['CONTACT_EMAIL']

    return render_template('contact.jinja', contact_email=contact_email)
