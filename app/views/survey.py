from flask import Blueprint, render_template
from flask_login import current_user
from flask_security import auth_required

from app.forms.survey import SurveyForm
from app.models import Survey

bp = Blueprint('survey', __name__)


@bp.route('/survey', methods=['GET', 'POST'])
@auth_required()
def get_post():

    # check if the user has completed the survey
    survey = Survey.query.filter_by(user_id=current_user.id).first()

    if survey:
        pass
        # return redirect

    form = SurveyForm()

    if form.validate_on_submit():
        pass

    return render_template('survey.jinja', form=form)
