from flask import Blueprint, render_template
from flask_security import auth_required

bp = Blueprint('game', __name__)


@bp.route('/game', methods=['GET', 'POST'])
@auth_required()
def get_post():
    return render_template('game.jinja')
