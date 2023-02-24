from flask import Blueprint, render_template
from flask_security import auth_required

bp = Blueprint('statistics', __name__)


@bp.route('/statistics', methods=['GET'])
@auth_required()
def get():
    # TODO overall statistics
    return render_template('statistics.jinja')
