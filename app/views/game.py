from flask import Blueprint, render_template, abort
from flask_login import current_user
from flask_security import auth_required

from app.forms.game import GameForm
from app.models import Config, UserResults, CaseGrouping, Patients, OrtData
from app.utils.random_case import get_random_patient_id

bp = Blueprint('game', __name__)


@bp.route('/game/<string:mode>', methods=['GET', 'POST'])
@auth_required()
def get_post(mode: str):

    # TODO round_id (new endpoint for results, round_id as a parameter)

    if mode not in ['classic', 'educational', 'time-limited']:
        abort(404)

    # Answer form
    form = GameForm()

    # TODO validate_on_submit
    if form.validate_on_submit():
        # TODO screen_size, mode, redirect to results if hidden field...
        pass

    # Get id's of already done cases
    done = UserResults.query.with_entities(UserResults.patient_id).filter_by(user_id=current_user.id).all()
    done = [result[0] for result in done]

    # Check if grouping mode is on and select case
    config = Config.query.filter_by(name='grouping_mode_on').one_or_none()
    if config and config.value:
        # Grouping mode on (selection based on group number)
        group_numbers = CaseGrouping.query.with_entities(CaseGrouping.group_nr)\
                                          .distinct(CaseGrouping.group_nr)\
                                          .order_by(CaseGrouping.group_nr).all()

        selected_patient_id = None
        for group_nr in group_numbers:
            selected_patient_id = get_random_patient_id(excluded=done, group_nr=group_nr[0])
            if selected_patient_id:
                break

        if not selected_patient_id:
            selected_patient_id = get_random_patient_id(excluded=done)

    else:
        # Random selection
        selected_patient_id = get_random_patient_id(excluded=done)

    # Collecting data from the database
    if selected_patient_id:
        selected_patient = Patients.query.filter_by(id=selected_patient_id).one_or_none()
        ort_data = OrtData.query.filter_by(patient_id=selected_patient_id).all()

        if not selected_patient or not ort_data or len(ort_data) != 3:
            return render_template('game.jinja', database_error=True)

        return render_template('game.jinja', selected_patient=selected_patient, ort_data=ort_data)
    else:
        return render_template('game.jinja', all_done=True)
