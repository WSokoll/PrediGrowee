import os
import re
from datetime import datetime

from flask import Blueprint, render_template, abort, current_app, redirect, url_for, session, send_file, flash
from flask_login import current_user
from flask_security import auth_required, logout_user
from sqlalchemy import and_, or_

from app.app import db
from app.forms.game import GameForm, DIRECTION_CHOICES
from app.models import Config, UserResults, CaseGrouping, Patients, OrtData, OrtParameters
from app.utils.random_case import get_random_patient_id

bp = Blueprint('game', __name__)


@bp.route('/game/<string:mode>', methods=['GET', 'POST'])
@auth_required()
def get_post(mode: str):

    if mode not in ['classic', 'educational', 'time-limited']:
        abort(404)

    # Answer form
    form = GameForm()

    # Time limit for time-limited mode
    time_limit = 30
    if mode == 'time-limited':
        time_limit_from_config = Config.query.filter_by(name='time_limit').one_or_none()
        time_limit = time_limit_from_config.int_value if time_limit_from_config else 30

    # Check if time's out in the time limited mode
    time_out = bool(
        mode == 'time-limited' and
        form.is_submitted() and
        not form.validate_on_submit() and
        form.direction.data is None and
        'time_start' in session and
        (datetime.now() - session['time_start'].replace(tzinfo=None)).total_seconds() >= time_limit
    )

    # Saving answer after validation or time_out
    if form.validate_on_submit() or time_out:

        # Extra show_result field validation in case of time out
        if time_out and not form.show_results.validate(form):
            abort(400)

        # Checking patient id and time_start saved in the session
        if 'patient_id' not in session or 'time_start' not in session:
            abort(400)

        patient = Patients.query.filter_by(id=session['patient_id']).one_or_none()
        db_check_result = db.session.query(UserResults.query.filter_by(patient_id=session['patient_id'],
                                                                       user_id=current_user.id).exists()).scalar()

        if db_check_result or (not patient):
            abort(400)

        # Save result to the database
        result = UserResults(
            user_id=current_user.id,
            patient_id=session['patient_id'],
            answer=None if time_out else DIRECTION_CHOICES[int(form.direction.data)][1],
            answer_correct=False if time_out else bool(patient.direction_of_growth == DIRECTION_CHOICES[int(form.direction.data)][1]),
            answer_date=datetime.now(),
            game_mode=mode,
            time_spent=(datetime.now() - session['time_start'].replace(tzinfo=None)).total_seconds(),
            round_id=current_user.round_id,
            round_token=current_user.round_token,
            screen_size=form.screen_size.data if re.match(r'^[0-9]{1,6}x[0-9]{1,6}$', form.screen_size.data) else None
        )

        db.session.add(result)
        db.session.commit()

        if form.show_results.data == 'true' or mode == 'educational':
            return redirect(url_for('results.get'))
        else:
            return redirect(url_for('game.get_post', mode=mode))

    # Get id's of already done cases
    done = UserResults.query.with_entities(UserResults.patient_id).filter_by(user_id=current_user.id).all()
    done = [result[0] for result in done]

    # Check if grouping mode is on and select case
    config = Config.query.filter_by(name='grouping_mode_on').one_or_none()
    if config and config.bool_value:
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

        # Check for warnings (between 1 and 3 -> display warning, more than 3 -> logout) <- time between downloads
        warning = False
        if 'download' in session:
            if 1 <= session['download']['warnings'] <= 3 and \
                    (datetime.now() - session['download']['last'].replace(tzinfo=None)).total_seconds() <= 5:
                warning = True
            elif session['download']['warnings'] > 3:
                session['download']['warnings'] = 0
                logout_user()
                return redirect(url_for('game.get_post', mode=mode))

        # Ort parameters download (columns in the table) from the database
        parameters = OrtParameters.query.order_by(OrtParameters.id).all()
        if not parameters or len(parameters) != 15:
            return render_template('game.jinja', database_error=True)

        return render_template('game.jinja',
                               form=form,
                               mode=mode,
                               time_limit=time_limit,
                               warning=warning,
                               selected_patient=selected_patient,
                               ort_data=ort_data,
                               parameters=parameters)
    else:
        return render_template('game.jinja', all_done=True)


@bp.route('/game/photo/<string:ort_id>', methods=['GET'])
@auth_required()
def get_photo(ort_id: str):

    # Warning and logout system - if user downloads photos too fast (less than 5 sec between)
    if 'download' in session:
        if (datetime.now() - session['download']['last'].replace(tzinfo=None)).total_seconds() <= 5:
            warnings = session['download']['warnings'] + 1
        else:
            warnings = 0
    else:
        warnings = 0

    session['download'] = {
        'last': datetime.now(),
        'warnings': warnings
    }

    ort_path = OrtData.query.with_entities(OrtData.path).filter_by(id=ort_id).one_or_none()

    if not ort_path:
        abort(404)

    ort_path = ort_path[0] if ort_path[0][0] != '\\' else ort_path[0][1:]
    path = os.path.join(current_app.config['ORT_FOLDER_PATH'], ort_path)

    if not os.path.exists(path):
        abort(404)

    return send_file(path)
