import os
from secrets import token_urlsafe

from flask import Blueprint, render_template, abort, current_app, send_file, flash, redirect, url_for
from flask_login import current_user
from flask_mail import Message
from flask_security import auth_required
from sqlalchemy import or_, and_

from app.app import db, mail
from app.models import UserResults, OrtData, User, Patients

bp = Blueprint('results', __name__)


@bp.route('/results', methods=['GET'])
@bp.route('/results/<string:round_token>', methods=['GET'])
@auth_required()
def get(round_token: str = None):

    # Case when results page is loaded from the link sent by mail
    if round_token:
        results = UserResults.query.filter_by(user_id=current_user.id, round_token=round_token).all()
        increment = False

    else:
        results = UserResults.query.filter_by(user_id=current_user.id, round_id=current_user.round_id).all()
        increment = True

        # If no results try round_id - 1 and do not increment round_id (protection against blank page after refresh)
        if not results:
            results = UserResults.query.filter_by(user_id=current_user.id, round_id=(current_user.round_id - 1)).all()
            increment = False

    # Percentage of correct answers
    correct_answer_percentage = 0

    if results:
        results_list = []
        for result in results:
            # Ort_ids -> to download necessary photos
            ort_ids = OrtData.query.with_entities(OrtData.age, OrtData.id)\
                .filter_by(patient_id=result.patient_id).order_by(OrtData.age).all()
            ort_ids = {p[0]: p[1] for p in ort_ids}

            patient = Patients.query.filter_by(id=result.patient_id).first()

            res_item = {
                'patient_id': result.patient_id,
                'sex': patient.sex,
                'answer': result.answer or '-',
                'answer_correct_bool': result.answer_correct,
                'correct_answer': patient.direction_of_growth,
                'time_spent': result.time_spent,
                'game_mode': result.game_mode,
                'round_token': result.round_token,
                'ort_ids': ort_ids,
                'list_of_age': [key for key, value in ort_ids.items()]
            }
            results_list.append(res_item)

            if result.answer_correct:
                correct_answer_percentage += 1

        correct_answer_percentage = int(correct_answer_percentage / len(results) * 100)

        # Increment round_id and change round_token
        if increment:
            user = User.query.filter_by(id=current_user.id).first()

            user.round_id += 1
            user.round_token = token_urlsafe(32)[:16]

            db.session.commit()

        return render_template('results.jinja', results=results_list, percentage=correct_answer_percentage)

    else:
        return render_template('results.jinja', no_results=True)


@bp.route('/results/photo/<string:ort_id>', methods=['GET'])
@auth_required()
def get_photo(ort_id: str):

    ort_data = OrtData.query.filter_by(id=ort_id).one_or_none()

    if not ort_data:
        abort(404)

    # Check if the user really solved the case related to the photo (also round_id or (round_id - 1) should match)
    patient_ids = UserResults.query.with_entities(UserResults.patient_id).filter(and_(
        or_(
            UserResults.round_id == current_user.round_id,
            UserResults.round_id == current_user.round_id - 1)
        ), UserResults.user_id == current_user.id
    ).all()

    patient_ids = [data[0] for data in patient_ids]

    if ort_data.patient_id not in patient_ids:
        abort(400)

    ort_path = ort_data.path if ort_data.path[0] != '\\' else ort_data.path[1:]
    ort_path = ort_path.replace('\\', '/')

    path = os.path.join(current_app.config['ORT_FOLDER_PATH'], ort_path)

    if not os.path.exists(path):
        abort(404)

    return send_file(path)


@bp.route('/results/email/<string:mode>/<string:round_token>/<int:solved>/<int:percentage>', methods=['GET'])
@auth_required()
def send_email(mode: str, round_token: str, solved: int, percentage: int):
    msg = Message(
        subject='Your results from PrediGrowee!',
        recipients=[current_user.email],
        html=render_template(
            'email/results.html',
            mode=mode,
            round_token=round_token,
            solved=solved,
            percentage=percentage
        )
    )

    mail.send(msg)
    flash('We send an email with the results and link to this page so you can come back any time.')
    # return 'Email sent', 204
    return redirect(url_for('results.get'))
