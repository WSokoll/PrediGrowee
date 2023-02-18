from flask import Blueprint, render_template
from flask_login import current_user
from flask_security import auth_required

from app.app import db
from app.models import UserResults, OrtData, User

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
            photo_paths = OrtData.query.with_entities(OrtData.age, OrtData.path)\
                .filter_by(patient_id=result.patient_id).order_by(OrtData.age).all()
            photo_paths = [{p[0]: p[1]} for p in photo_paths]

            # TODO correct answer
            res_item = {
                'patient_id': result.patient_id,
                'answer': result.answer,
                'answer_correct_bool': result.answer_correct,
                'correct_answer': 'testtt',
                'time_spent': result.time_spent,
                'photo_paths': photo_paths
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
