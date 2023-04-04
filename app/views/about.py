from flask import Blueprint, render_template

from app.models import OrtParameters, AboutContent

bp = Blueprint('about', __name__)


@bp.route('/about', methods=['GET'])
def get():

    content = AboutContent.query.order_by(AboutContent.id).all()
    parameters = OrtParameters.query.order_by(OrtParameters.id).all()

    return render_template('about.jinja', content=content, id_list=[c.id for c in content], parameters=parameters)
