from flask import Blueprint, render_template

bp = Blueprint('contact', __name__)


@bp.route('/contact', methods=['GET'])
def get():
    return render_template('contact.jinja')
