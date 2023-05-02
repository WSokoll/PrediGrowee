from flask import Blueprint, render_template, abort

from app.models import Config

bp = Blueprint('privacy', __name__)


@bp.route('/privacy', methods=['GET'])
def get():

    privacy_content = Config.query.filter_by(name='privacy_content').one_or_none()
    if not privacy_content:
        abort(404)

    return render_template('privacy.jinja', content=privacy_content.string_value)
