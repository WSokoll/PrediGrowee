from flask import Blueprint, render_template
from flask_login import current_user
from flask_security import auth_required

from app.app import db

bp = Blueprint('statistics', __name__)


@bp.route('/statistics', methods=['GET'])
@auth_required()
def get():
    statistics = {
        'time-limited': {
            'count_all': 0,
            'count_correct': 0,
            'sum_time': 0
        },
        'educational': {
            'count_all': 0,
            'count_correct': 0,
            'sum_time': 0
        },
        'classic': {
            'count_all': 0,
            'count_correct': 0,
            'sum_time': 0
        }
    }

    for game_mode in ['classic', 'educational', 'time-limited']:
        query = db.session.execute(
            """
            SELECT COALESCE(COUNT(id), 0) AS count_all, 
                   COALESCE(SUM(answer_correct), 0) AS count_correct,
                   COALESCE(SUM(time_spent), 0) AS sum_time 
            FROM user_results 
            WHERE user_id = :user_id AND game_mode = :game_mode
            """,
            {'user_id': current_user.id, 'game_mode': game_mode})

        for key, value in query.mappings().all()[0].items():
            statistics[game_mode][key] = value

    return render_template('statistics.jinja', statistics=statistics)
