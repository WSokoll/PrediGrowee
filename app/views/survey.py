from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from flask_security import auth_required

from app.app import db
from app.forms.survey import SurveyForm
from app.models import Survey

bp = Blueprint('survey', __name__)


@bp.route('/survey', methods=['GET', 'POST'])
@auth_required()
def get_post():

    # check if the user has completed the survey
    survey = Survey.query.filter_by(user_id=current_user.id).first()

    if survey:
        return redirect(url_for('game.get_post'))

    form = SurveyForm()

    if form.validate_on_submit():
        survey = Survey(
            user_id=current_user.id,
            gender=form.gender.data,
            age=form.age.data,
            vision_defect=form.vision_defect.data,
            education=form.education_other.data if form.education.data == 'other' else form.education.data,
            experience=form.experience.data
        )

        db.session.add(survey)
        db.session.commit()

        return redirect(url_for('game.get_post'))

    return render_template('survey.jinja', form=form)
