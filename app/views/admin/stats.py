from datetime import datetime, timedelta

from flask_admin import BaseView, expose


class StatsBaseView(BaseView):

    def __init__(self, session, models, *args, **kwargs):
        self.session = session
        self.models = models
        super(StatsBaseView, self).__init__(*args, **kwargs)

    @expose('/')
    def index(self):

        # OVERALL STATS
        collected_data_query = self.session.execute(
            """
            SELECT COALESCE(COUNT(*), 0) AS count_all,
                   COALESCE((SELECT COUNT(*) FROM user_results WHERE answer_correct = TRUE), 0) AS count_correct,
                   COALESCE(AVG(time_spent), 0) AS avg_time,
                   COALESCE((SELECT COUNT(*) FROM user_results WHERE game_mode = 'classic'), 0) AS count_classic,
                   COALESCE((SELECT COUNT(*) FROM user_results WHERE game_mode = 'educational'), 0) AS count_educational,
                   COALESCE((SELECT COUNT(*) FROM user_results WHERE game_mode = 'time-limited'), 0) AS count_time_lim
            FROM user_results
            """)

        login_stats_query = self.session.execute(
            """
            SELECT COALESCE(COUNT(*), 0) AS count_all,
                   COALESCE((SELECT COUNT(*) FROM survey), 0) AS count_surveys, 
                   COALESCE(SUM(login_count + login_google_count), 0) AS login_sum,
                   COALESCE(SUM(login_google_count), 0) AS login_google_sum,
                   COALESCE(AVG(login_count + login_google_count), 0) AS avg_login
            FROM user
            """)

        coll_data = collected_data_query.mappings().all()[0]
        login_data = login_stats_query.mappings().all()[0]

        overall_stats = {
            'Collected data stats': {
                'Number of collected answers': coll_data['count_all'],
                'Number of cases solved correctly': coll_data['count_correct'],
                'Average time a user spends solving a single case [sec]': coll_data['avg_time'],
                'Number of cases solved in the Classic Mode': coll_data['count_classic'],
                'Number of cases solved in the Educational Mode': coll_data['count_educational'],
                'Number of cases solved in the Time Limited Mode': coll_data['count_time_lim']
            },
            'Login and registration stats': {
                'Number of accounts registered': login_data['count_all'],
                'Number of completed initial surveys': login_data['count_surveys'],
                'Total number of logins to the app': login_data['login_sum'],
                'Total number of logins via Google to the app': login_data['login_google_sum'],
                'Average number of logins to the app by one user': login_data['avg_login']
            }
        }

        # CHART DATA
        chart_data = {}

        answer_dates = self.models.UserResults.query\
            .with_entities(self.models.UserResults.answer_date)\
            .order_by(self.models.UserResults.answer_date)\
            .all()

        answer_dates = [query_result[0].date() for query_result in answer_dates]

        answer_date_counts = {}
        date_form_past = datetime.now().date() - timedelta(days=365)
        while datetime.now().date() >= date_form_past:
            answer_date_counts[date_form_past] = 0
            date_form_past += timedelta(days=1)

        for date in answer_dates:
            answer_date_counts[date] = answer_date_counts.get(date, 0) + 1

        date_labels = sorted(answer_date_counts.keys())

        chart_data["answer_counts"] = [answer_date_counts[label] for label in date_labels]
        chart_data["date_labels"] = [date.strftime("%Y-%m-%d") for date in date_labels]

        correctly_solved_count = self.models.UserResults.query.filter_by(answer_correct=True).count()
        incorrectly_solved_count = self.models.UserResults.query.filter_by(answer_correct=False).count()

        chart_data["correctly_solved_percentage"] = \
            int((correctly_solved_count / (correctly_solved_count + incorrectly_solved_count)) * 100)

        # FIRST GROUP STATS (if grouping_mode on)
        first_group_stats = {}
        mode_on_check = self.models.Config.query.filter_by(name='grouping_mode_on').one_or_none()
        if mode_on_check and mode_on_check.bool_value:
            first_group_patients = self.models.CaseGrouping.query.filter_by(group_nr=1).all()

            for case in first_group_patients:
                query = self.session.execute(
                    """
                    SELECT COALESCE(COUNT(*), 0) AS count_all,
                           COALESCE((SELECT COUNT(*) FROM user_results 
                           WHERE answer_correct = TRUE AND patient_id = :patient_id), 0) AS count_correct
                    FROM user_results
                    WHERE patient_id = :patient_id
                    """,
                    {'patient_id': case.patient_id})

                data = query.mappings().all()[0]
                first_group_stats[case.patient_id] = {
                    'count_all': data['count_all'],
                    'count_correct': data['count_correct']
                }

            return self.render('admin/views/stats.html',
                               overall_stats=overall_stats,
                               first_group_stats=first_group_stats,
                               chart_data=chart_data)

        return self.render('admin/views/stats.html',
                           overall_stats=overall_stats,
                           chart_data=chart_data)
