from flask import Blueprint, render_template

bp = Blueprint('login', __name__)


@bp.route('/login', methods=['GET'])
def login():
    return render_template('login.jinja')
