from flask import Blueprint, render_template

from app.models import OrtParameters

bp = Blueprint('parameters', __name__)


@bp.route('/parameters', methods=['GET'])
def get():
    parameters = OrtParameters.query.order_by(OrtParameters.id).all()
    return render_template('parameters.jinja', parameters=parameters)
