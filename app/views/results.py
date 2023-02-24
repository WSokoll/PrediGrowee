import os

from flask import Blueprint, render_template, abort, current_app, send_file
from flask_login import current_user
from flask_security import auth_required
from sqlalchemy import or_, and_

from app.app import db
from app.models import UserResults, OrtData, User, Patients

bp = Blueprint('results', __name__)


@bp.route('/results', methods=['GET', 'POST'])
@auth_required()
def get():
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

            patient_sex = (Patients.query.with_entities(Patients.sex).filter_by(id=result.patient_id).first())[0]

            # TODO correct answer
            res_item = {
                'patient_id': result.patient_id,
                'sex': patient_sex,
                'answer': result.answer,
                'answer_correct_bool': result.answer_correct,
                'correct_answer': 'predominantly test',
                'time_spent': result.time_spent,
                'ort_ids': ort_ids
            }
            results_list.append(res_item)

            if result.answer_correct:
                correct_answer_percentage += 1

        correct_answer_percentage = int(correct_answer_percentage / len(results) * 100)

        # Increment round_id
        if increment:
            user = User.query.filter_by(id=current_user.id).first()
            user.round_id += 1
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
    path = os.path.join(current_app.config['ORT_FOLDER_PATH'], ort_path)

    if not os.path.exists(path):
        abort(404)

    return send_file(path)
