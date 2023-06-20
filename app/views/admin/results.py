from flask_admin.contrib.sqla import ModelView


class ResultsModelView(ModelView):
    can_view_details = True
    can_create = False
    can_edit = False
    can_delete = True

    column_list = ['id', 'user_id', 'user.email', 'time_spent']
    column_sortable_list = ['id', 'user_id', 'user.email', 'time_spent']
    column_details_list = ['id', 'user_id', 'user.email', 'screen_size', 'time_spent']

    column_labels = {
        'id': 'ID',
        'user_id': 'User ID',
        'user.email': 'User email',
        'time_spent': 'Time spent [s]',
        'screen_size': 'Screen size'
    }
