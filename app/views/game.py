import os
import re
from datetime import datetime

from flask import Blueprint, render_template, abort, current_app, redirect, url_for, session, send_file
from flask_login import current_user
from flask_security import auth_required
from sqlalchemy import and_, or_

from app.app import db
from app.forms.game import GameForm, DIRECTION_CHOICES
from app.models import Config, UserResults, CaseGrouping, Patients, OrtData
from app.utils.random_case import get_random_patient_id

bp = Blueprint('game', __name__)


@bp.route('/game/<string:mode>', methods=['GET', 'POST'])
@auth_required()
def get_post(mode: str):

    if mode not in ['classic', 'educational', 'time-limited']:
        abort(404)

    # Answer form
    form = GameForm()

    # Saving answer after validation
    if form.validate_on_submit():

        # Checking patient id and time_start saved in the session
        if 'patient_id' not in session or 'time_start' not in session:
            abort(400)

        db_check_patient = db.session.query(Patients.query.filter_by(id=session['patient_id']).exists()).scalar()
        db_check_result = db.session.query(UserResults.query.filter_by(patient_id=session['patient_id']).exists()).scalar()

        if db_check_result or (not db_check_patient):
            abort(400)

        # Save result to the database
        result = UserResults(
            user_id=current_user.id,
            patient_id=session['patient_id'],
            answer=DIRECTION_CHOICES[int(form.direction.data)][1],
            answer_correct=True,  # TODO answer correct
            answer_date=datetime.now(),
            game_mode=mode,
            time_spent=(datetime.now() - session['time_start'].replace(tzinfo=None)).total_seconds(),
            round_id=current_user.round_id,
            screen_size=form.screen_size.data if re.match(r'^[0-9]{1,6}x[0-9]{1,6}$', form.screen_size.data) else None
        )

        db.session.add(result)
        db.session.commit()

        if form.show_results.data == 'true':
            return redirect(url_for('results.get'))
        else:
            return redirect(url_for('game.get_post', mode=mode))

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
        ort_data = OrtData.query.filter(and_(
            OrtData.patient_id == selected_patient_id,
            or_(OrtData.photo_number == 1, OrtData.photo_number == 2)
        )).all()

        if not selected_patient or not ort_data or len(ort_data) != 2:
            return render_template('game.jinja', database_error=True)

        ort_data = {data.photo_number: data for data in ort_data}

        # Storing patient id and time for time_spent calculation in the session
        session['patient_id'] = selected_patient_id
        session['time_start'] = datetime.now()

        return render_template('game.jinja',
                               form=form,
                               mode=mode,
                               selected_patient=selected_patient,
                               ort_data=ort_data,
                               columns=current_app.config['ORT_DATA_COLUMNS'])
    else:
        return render_template('game.jinja', all_done=True)


@bp.route('/game/photo/<string:ort_id>', methods=['GET'])
@auth_required()
def get_photo(ort_id: str):
    # TODO time between downloads - warning, block

    ort_data = OrtData.query.filter_by(id=ort_id).one_or_none()

    if not ort_data:
        abort(404)

    ort_path = ort_data.path if ort_data.path[0] != '\\' else ort_data.path[1:]
    path = os.path.join(current_app.config['ORT_FOLDER_PATH'], ort_path)

    if not os.path.exists(path):
        abort(404)

    return send_file(path)
