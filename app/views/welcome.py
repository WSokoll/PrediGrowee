from flask import Blueprint, render_template

bp = Blueprint('welcome', __name__)


@bp.route('/', methods=['GET'])
@bp.route('/welcome', methods=['GET'])
def welcome():
    return render_template('welcome.jinja')
