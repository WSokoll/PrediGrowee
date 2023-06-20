from flask import Blueprint, render_template, current_app

bp = Blueprint('contact', __name__)


@bp.route('/contact', methods=['GET'])
def get():
    contact_email = current_app.config['CONTACT_EMAIL']
    contact_email_2 = current_app.config['CONTACT_EMAIL_2']

    return render_template('contact.jinja', contact_email=contact_email, contact_email_2=contact_email_2)
